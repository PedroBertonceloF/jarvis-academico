from __future__ import annotations

import json
import os
import re
import time
from datetime import date
from typing import Any

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    OpenAI,
)

from .config import settings


def _limpar_env(valor: str | None) -> str:
    """Remove espaços, quebras de linha e aspas acidentais vindas do painel de deploy."""
    return str(valor or "").strip().strip("\'").strip('"').strip()


def _env_int(nome: str, padrao: int) -> int:
    try:
        return int(_limpar_env(os.getenv(nome)) or padrao)
    except (TypeError, ValueError):
        return padrao


def _resumir_erro(exc: Exception, limite: int = 500) -> str:
    partes = []
    atual: BaseException | None = exc
    while atual is not None and len(partes) < 4:
        texto = str(atual).strip()
        if texto:
            partes.append(f"{atual.__class__.__name__}: {texto}")
        atual = atual.__cause__
    return compactar_texto(" | ".join(partes) or exc.__class__.__name__, limite=limite)


class GemmaClient:
    """Cliente OpenAI-compatible para a LLM remota usada no trabalho.

    Também oferece diagnóstico de conectividade para deploy online.
    O nome da classe e das variáveis GEMMA_* é mantido por compatibilidade
    com o histórico do projeto e com o Space já configurado.

    Variáveis úteis:
    - GEMMA_TIMEOUT_SECONDS: tempo máximo de chamada à API.
    - GEMMA_MAX_TOKENS: limite superior de tokens por resposta.
    """

    def __init__(self) -> None:
        settings.validate_llm()
        self.model = _limpar_env(settings.gemma_model)
        self.mock = settings.usando_mock
        self.base_url = _limpar_env(settings.gemma_base_url)
        self.api_key = _limpar_env(settings.gemma_api_key)
        self.provider = settings.llm_provider
        self.provider_label = self.model or settings.llm_provider_label
        self.timeout_seconds = _env_int("GEMMA_TIMEOUT_SECONDS", 180)
        self.max_tokens_limit = _env_int("GEMMA_MAX_TOKENS", 512)

        self.client = None
        if not self.mock:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
                timeout=self.timeout_seconds,
                max_retries=0,
            )

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.2, max_tokens: int = 350) -> str:
        if self.mock:
            return self._chat_mock(messages)

        efetivo_max_tokens = max(1, min(int(max_tokens), int(self.max_tokens_limit)))

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=efetivo_max_tokens,
                timeout=self.timeout_seconds,
            )
            return response.choices[0].message.content or ""
        except APITimeoutError as exc:
            raise TimeoutError(
                f"Timeout ao chamar a API LLM após {self.timeout_seconds}s. "
                "A API externa não respondeu dentro do limite configurado. "
                f"Detalhe técnico: {_resumir_erro(exc)}"
            ) from exc
        except AuthenticationError as exc:
            raise PermissionError(
                "Token da API LLM inválido ou recusado. "
                "Confira o Secret GEMMA_API_KEY, sem aspas e sem 'GEMMA_API_KEY=' no valor. "
                f"Detalhe técnico: {_resumir_erro(exc)}"
            ) from exc
        except APIConnectionError as exc:
            raise ConnectionError(
                "Falha de conexão com a API LLM. "
                "Confira se o ambiente online consegue acessar GEMMA_BASE_URL. "
                f"Detalhe técnico: {_resumir_erro(exc)}"
            ) from exc
        except APIStatusError as exc:
            raise RuntimeError(
                f"Erro HTTP da API LLM: status={exc.status_code}, resposta={exc.response.text[:500]}. "
                f"Detalhe técnico: {_resumir_erro(exc)}"
            ) from exc

    def ping(self, prompt: str = "Responda apenas: OK") -> dict[str, Any]:
        """Teste direto da LLM remota, sem RAG, sem tool calling e sem agente."""
        inicio = time.perf_counter()

        if self.mock:
            return {
                "ok": True,
                "modo": "mock",
                "provider": self.provider,
                "llm_provider_label": self.provider_label,
                "resposta": "OK MOCK",
                "response_preview": "OK MOCK",
                "elapsed_seconds": round(time.perf_counter() - inicio, 3),
                "base_url": self.base_url,
                "model": self.model,
                "api_key_presente": bool(self.api_key),
                "timeout_seconds": self.timeout_seconds,
                "max_tokens_limit": self.max_tokens_limit,
            }

        resposta = self.chat(
            [{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=min(20, self.max_tokens_limit),
        )
        return {
            "ok": True,
            "modo": settings.llm_mode,
            "provider": self.provider,
            "llm_provider_label": self.provider_label,
            "resposta": resposta,
            "response_preview": compactar_texto(resposta, limite=160),
            "elapsed_seconds": round(time.perf_counter() - inicio, 3),
            "base_url": self.base_url,
            "model": self.model,
            "api_key_presente": bool(self.api_key),
            "timeout_seconds": self.timeout_seconds,
            "max_tokens_limit": self.max_tokens_limit,
        }

    def _chat_mock(self, messages: list[dict[str, str]]) -> str:
        ultimo = messages[-1].get("content", "") if messages else ""
        texto = ultimo.lower()

        # 1) Simula a decisão de tool calling.
        if "planejador de ferramentas" in texto or "ferramentas disponíveis" in texto:
            mensagem = self._extrair_mensagem_usuario(ultimo)
            chamadas = self._decidir_ferramentas_mock(mensagem)
            return json.dumps(chamadas, ensure_ascii=False)

        # 2) Simula geração de pergunta de active recall.
        if "crie uma pergunta objetiva de active recall" in texto:
            return (
                "Pergunta: Explique, com suas palavras, por que o RAG reduz alucinações em respostas de LLMs.\n\n"
                "Resposta esperada: Porque o modelo não responde apenas com base no seu conhecimento interno; "
                "ele primeiro recupera trechos relevantes de uma base de documentos e usa esses trechos como contexto."
            )

        # 3) Simula avaliação interativa.
        if "avalie a resposta do estudante" in texto:
            return (
                "Classificação: parcialmente correta.\n\n"
                "Pontos fortes: a resposta mostra entendimento geral do tema.\n\n"
                "Correção objetiva: complemente citando que o RAG combina recuperação de documentos com geração de texto, "
                "e que a resposta deve ficar ancorada nos trechos recuperados.\n\n"
                "Recomendação de revisão: revise RAG, chunking, embeddings e busca híbrida."
            )

        # 4) Simula resposta final usando resultados das ferramentas.
        if "resultados das ferramentas:" in texto:
            return self._responder_final_mock(ultimo)

        return (
            "Modo teste sem LLM remota ativo. Consigo validar o fluxo do sistema, mas a resposta final oficial "
            "deve ser testada depois com o token do professor e LLM_MODE=gemma ou LLM_MODE=qwen."
        )

    def _extrair_mensagem_usuario(self, prompt: str) -> str:
        match = re.search(r"Mensagem do usuário:\s*(.+)", prompt, flags=re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else prompt.strip()

    def _decidir_ferramentas_mock(self, mensagem: str) -> list[dict[str, Any]]:
        m = mensagem.lower()
        hoje = date.today().isoformat()

        if any(p in m for p in ["avaliar minha resposta", "avalie minha resposta", "corrija minha resposta"]):
            return [{"tool": "avaliar_resposta_revisao", "args": {"resposta_aluno": mensagem}}]

        if any(p in m for p in ["revisão ativa", "revisao ativa", "active recall", "sessão de revisão", "sessao de revisao"]):
            tema = mensagem
            for termo in ["sobre", "de"]:
                if termo in m:
                    tema = mensagem.split(termo, 1)[-1].strip()
                    break
            return [{"tool": "iniciar_revisao", "args": {"disciplina": "Inteligência Artificial", "tema": tema}}]

        if any(p in m for p in ["registrar dificuldade", "tenho dificuldade", "minha dificuldade"]):
            topico = mensagem
            for termo in ["em", "sobre"]:
                if termo in m:
                    topico = mensagem.split(termo, 1)[-1].strip()
                    break
            return [{"tool": "registrar_dificuldade", "args": {"disciplina": "Inteligência Artificial", "topico": topico}}]

        if any(p in m for p in ["listar dificuldades", "minhas dificuldades", "dificuldades registradas"]):
            return [{"tool": "listar_dificuldades", "args": {"limite": 10}}]

        if any(p in m for p in ["adicionar evento", "adicionar prova", "adicionar aula", "nova prova", "nova aula"]):
            return [{"tool": "adicionar_evento", "args": {"data": hoje, "titulo": mensagem, "tipo": "evento"}}]

        if any(p in m for p in ["concluir", "marcar", "finalizar"]):
            alvo = re.sub(r".*?(concluir|marcar|finalizar)( tarefa)?", "", mensagem, flags=re.IGNORECASE).strip()
            return [{"tool": "concluir_tarefa", "args": {"tarefa_id_ou_titulo": alvo or mensagem}}]

        if any(p in m for p in ["adicionar tarefa", "adicione tarefa", "nova tarefa", "criar tarefa"]):
            titulo = re.sub(r".*?(adicionar|adicione|nova|criar) tarefa", "", mensagem, flags=re.IGNORECASE).strip()
            titulo = re.split(r"\b(para|até|ate|amanhã|amanha)\b", titulo, flags=re.IGNORECASE)[0].strip(" :-")
            return [{"tool": "adicionar_tarefa", "args": {"titulo": titulo or mensagem, "prioridade": "média"}}]

        if "tarefa" in m or "pendência" in m or "pendencia" in m:
            return [{"tool": "listar_tarefas", "args": {"incluir_concluidas": False}}]

        if any(p in m for p in ["plano", "planej", "priorizar", "prioridade", "estudar hoje", "prova"]):
            return [{"tool": "planejar_estudos", "args": {"objetivo": mensagem, "dias": 3}}]

        if any(p in m for p in ["agenda", "aula", "tenho hoje", "o que tenho", "semana", "amanhã", "amanha"]):
            args: dict[str, Any] = {}
            if "hoje" in m:
                args["inicio"] = hoje
                args["fim"] = hoje
            if "prova" in m:
                args["termo"] = "prova"
            return [{"tool": "consultar_agenda", "args": args}]

        if any(p in m for p in ["exercício", "exercicio", "quiz", "pergunta", "active recall", "treinar"]):
            tema = mensagem
            for termo in ["sobre", "de"]:
                if termo in m:
                    tema = mensagem.split(termo, 1)[-1].strip()
                    break
            return [{"tool": "gerar_exercicios", "args": {"tema": tema, "quantidade": 3}}]

        if any(p in m for p in [
            "explique", "explica", "resuma", "defina", "o que é", "o que e", "como funciona",
            "material", "conceito", "conceitos", "rag", "bm25", "embedding", "embeddings", "faiss",
            "knn", "gradiente", "regressão", "regressao", "logística", "logistica", "heap", "grafos", "sql"
        ]):
            return [{"tool": "buscar_material_rag", "args": {"pergunta": mensagem, "metodo": "hibrido", "k": 3}}]

        return []

    def _responder_final_mock(self, prompt: str) -> str:
        try:
            raw = prompt.split("Resultados das ferramentas:", 1)[1].strip()
            resultados = json.loads(raw)
        except Exception:
            resultados = []

        if not resultados:
            return "Não precisei chamar ferramentas para responder em modo teste."

        partes = ["Modo teste sem LLM remota — ferramentas executadas com sucesso."]
        for item in resultados:
            tool = item.get("tool", "")
            saida = item.get("saida")
            if tool == "buscar_material_rag" and isinstance(saida, dict):
                if saida.get("resultado_vazio"):
                    partes.append(
                        "\nNão encontrei esse tema nos materiais cadastrados. "
                        "Vou responder com meu conhecimento geral da base de dados do modelo.\n\n"
                        "Em modo mock, o fallback geral foi acionado corretamente. "
                        "Na validação com a LLM remota, aqui será gerada uma explicação didática sobre o conceito solicitado.\n\n"
                        "Sugestão: importe um PDF, anotação ou material sobre esse tema para que respostas futuras sejam baseadas no RAG."
                    )
                else:
                    partes.append("\nResposta RAG: " + str(saida.get("resposta", "")))
                docs = saida.get("documentos_recuperados", [])
                if docs:
                    fontes = ", ".join(sorted({str(d.get("fonte", "")) for d in docs if d.get("fonte")}))
                    partes.append("Fontes recuperadas: " + fontes)
            elif tool == "consultar_agenda":
                partes.append("\nAgenda encontrada: " + self._resumir_objeto(saida))
            elif tool == "listar_tarefas":
                partes.append("\nTarefas encontradas: " + self._resumir_objeto(saida))
            elif tool == "adicionar_evento":
                partes.append("\nEvento adicionado: " + self._resumir_objeto(saida))
            elif tool == "adicionar_tarefa":
                partes.append("\nTarefa adicionada: " + self._resumir_objeto(saida))
            elif tool == "concluir_tarefa":
                partes.append("\nTarefa concluída: " + self._resumir_objeto(saida))
            elif tool == "planejar_estudos":
                partes.append("\nPlano base gerado com agenda, tarefas e materiais: " + self._resumir_objeto(saida))
            elif tool == "gerar_exercicios":
                partes.append(
                    "\nExercícios sugeridos:\n"
                    "1. Explique o conceito central do tema.\n"
                    "2. Cite uma vantagem e uma limitação.\n"
                    "3. Dê um exemplo aplicado ao trabalho prático."
                )
            elif tool == "iniciar_revisao":
                partes.append("\nRevisão ativa iniciada: " + self._resumir_objeto(saida))
            elif tool == "avaliar_resposta_revisao":
                partes.append("\nResposta avaliada: " + self._resumir_objeto(saida))
            elif tool == "registrar_dificuldade":
                partes.append("\nDificuldade registrada: " + self._resumir_objeto(saida))
            elif tool == "listar_dificuldades":
                partes.append("\nDificuldades registradas: " + self._resumir_objeto(saida))
            else:
                partes.append(f"\n{tool}: {self._resumir_objeto(saida)}")

        partes.append("\nNa entrega final, troque para LLM_MODE=gemma ou LLM_MODE=qwen e valide a geração real com a LLM remota.")
        return "\n".join(partes)

    def _resumir_objeto(self, obj: Any, limite: int = 1000) -> str:
        texto = json.dumps(obj, ensure_ascii=False, default=str)
        return compactar_texto(texto, limite=limite)


def compactar_texto(texto: str, limite: int = 4000) -> str:
    texto = " ".join(str(texto).split())
    if len(texto) <= limite:
        return texto
    return texto[:limite] + " [...]"
