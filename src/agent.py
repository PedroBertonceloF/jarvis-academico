from __future__ import annotations

from datetime import date
import json
import re
from typing import Any

from .llm_client import GemmaClient, compactar_texto
from .tools import TOOL_SPECS, ToolRegistry


class JarvisAgent:
    """Agente com tool calling decidido pela LLM.

    Estratégia usada:
    1. A LLM recebe a pergunta e a lista de ferramentas.
    2. A LLM deve devolver JSON com as chamadas necessárias.
    3. O Python executa as ferramentas e registra logs.
    4. A LLM gera a resposta final usando os resultados.
    """

    def __init__(self, tools: ToolRegistry | None = None) -> None:
        self.llm = GemmaClient()
        self.tools = tools or ToolRegistry()

    def responder(self, mensagem_usuario: str) -> dict[str, Any]:
        decisoes = self._decidir_ferramentas(mensagem_usuario)
        resultados = []

        for chamada in decisoes:
            nome = chamada.get("tool") or chamada.get("name")
            args = chamada.get("args", {}) or {}
            if not nome:
                continue
            saida = self.tools.executar(nome, args)
            resultados.append({"tool": nome, "args": args, "saida": saida})

        resposta_final = self._responder_final(mensagem_usuario, resultados)
        return {
            "resposta": resposta_final,
            "tool_calls": resultados,
        }

    def _decidir_ferramentas(self, mensagem_usuario: str) -> list[dict[str, Any]]:
        prompt = f"""
Hoje é {date.today().isoformat()}.
Você é o planejador de ferramentas do JARVIS Acadêmico.
Decida quais ferramentas devem ser chamadas para responder ao usuário.

Ferramentas disponíveis:
{json.dumps(TOOL_SPECS, ensure_ascii=False, indent=2)}

Regras obrigatórias:
- A decisão deve ser sua, não use lógica fixa.
- Responda SOMENTE com JSON válido.
- Se nenhuma ferramenta for necessária, responda: []
- Formato: [{{"tool": "nome_da_ferramenta", "args": {{...}}}}]
- Para perguntas sobre materiais/conteúdo/explicações, use buscar_material_rag.
- Para agenda, use consultar_agenda.
- Para tarefas, use listar_tarefas, adicionar_tarefa ou concluir_tarefa.
- Para plano/prioridade de estudos, use planejar_estudos.
- Para exercícios ou prática, use gerar_exercicios.

Mensagem do usuário: {mensagem_usuario}
""".strip()
        resposta = self.llm.chat([
            {"role": "system", "content": "Você escolhe ferramentas e responde apenas JSON."},
            {"role": "user", "content": prompt},
        ], temperature=0.0, max_tokens=250)
        return self._extrair_json_lista(resposta)

    def _extrair_json_lista(self, texto: str) -> list[dict[str, Any]]:
        texto = texto.strip()
        try:
            data = json.loads(texto)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            pass

        match = re.search(r"\[[\s\S]*\]", texto)
        if match:
            try:
                data = json.loads(match.group(0))
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                return []
        return []

    def _responder_final(self, mensagem_usuario: str, resultados: list[dict[str, Any]]) -> str:
        if not resultados:
            return self.llm.chat([
                {"role": "system", "content": "Você é o JARVIS Acadêmico, um assistente objetivo para estudantes."},
                {"role": "user", "content": mensagem_usuario},
            ])

        # Economia de tokens: se a única ferramenta foi RAG e ela já gerou a resposta,
        # devolvemos direto sem chamar a LLM novamente apenas para reescrever.
        if (
            len(resultados) == 1
            and resultados[0].get("tool") == "buscar_material_rag"
            and isinstance(resultados[0].get("saida"), dict)
            and resultados[0]["saida"].get("resposta")
        ):
            saida = resultados[0]["saida"]
            fontes = sorted({
                d.get("fonte", "")
                for d in saida.get("documentos_recuperados", [])
                if d.get("fonte")
            })
            sufixo = ("\n\nFontes recuperadas: " + ", ".join(fontes)) if fontes else ""
            return str(saida["resposta"]) + sufixo

        resultados_compactos = compactar_texto(json.dumps(resultados, ensure_ascii=False), limite=4500)
        prompt = f"""
Responda ao usuário de forma objetiva, acadêmica e útil.
Use os resultados das ferramentas abaixo. Quando houver documentos recuperados, cite o nome da fonte.

Pergunta do usuário:
{mensagem_usuario}

Resultados das ferramentas:
{resultados_compactos}
""".strip()
        return self.llm.chat([
            {"role": "system", "content": "Você é o JARVIS Acadêmico. Integre resultados das ferramentas sem inventar dados."},
            {"role": "user", "content": prompt},
        ], temperature=0.2, max_tokens=450)
