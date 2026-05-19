from __future__ import annotations

import json
import re
from datetime import date
from typing import Any

from openai import OpenAI

from .config import settings


class GemmaClient:
    """Cliente OpenAI-compatible para o Gemma 12B exigido no trabalho.

    Para desenvolvimento local sem o token do professor, use LLM_MODE=mock no .env.
    O modo mock não substitui a entrega final: ele apenas permite testar fluxo, RAG,
    agenda, tarefas, logs e interface enquanto o token oficial não chega.
    """

    def __init__(self) -> None:
        settings.validate_llm()
        self.model = settings.gemma_model
        self.mock = settings.usando_mock
        self.client = None if self.mock else OpenAI(base_url=settings.gemma_base_url, api_key=settings.gemma_api_key)

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.2, max_tokens: int = 350) -> str:
        if self.mock:
            return self._chat_mock(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

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
            "Modo teste sem Gemma ativo. Consigo validar o fluxo do sistema, mas a resposta final oficial "
            "deve ser testada depois com o token do professor e LLM_MODE=gemma."
        )

    def _extrair_mensagem_usuario(self, prompt: str) -> str:
        match = re.search(r"Mensagem do usuário:\s*(.+)", prompt, flags=re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else prompt.strip()

    def _decidir_ferramentas_mock(self, mensagem: str) -> list[dict[str, Any]]:
        m = mensagem.lower()
        hoje = date.today().isoformat()

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

        partes = ["Modo teste sem Gemma — ferramentas executadas com sucesso."]
        for item in resultados:
            tool = item.get("tool", "")
            saida = item.get("saida")
            if tool == "buscar_material_rag" and isinstance(saida, dict):
                if saida.get("resultado_vazio"):
                    partes.append(
                        "\nNão encontrei esse tema nos materiais cadastrados. "
                        "Vou responder com meu conhecimento geral da base de dados do modelo.\n\n"
                        "Em modo mock, o fallback geral foi acionado corretamente. "
                        "Na validação com Gemma, aqui será gerada uma explicação didática sobre o conceito solicitado.\n\n"
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
            else:
                partes.append(f"\n{tool}: {self._resumir_objeto(saida)}")

        partes.append("\nNa entrega final, troque para LLM_MODE=gemma e valide a geração real com Gemma 12B.")
        return "\n".join(partes)

    def _resumir_objeto(self, obj: Any, limite: int = 1000) -> str:
        texto = json.dumps(obj, ensure_ascii=False, default=str)
        return compactar_texto(texto, limite=limite)


def compactar_texto(texto: str, limite: int = 4000) -> str:
    texto = " ".join(str(texto).split())
    if len(texto) <= limite:
        return texto
    return texto[:limite] + " [...]"
