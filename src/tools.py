from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Callable

from .logger import registrar_tool_call
from .rag import RagEngine
from .storage import AgendaStore, EventoAgenda, Tarefa, TarefaStore


TOOL_SPECS = [
    {
        "name": "consultar_agenda",
        "description": "Consulta eventos da agenda acadêmica por período ou termo.",
        "args": {
            "inicio": "Data inicial no formato AAAA-MM-DD, opcional.",
            "fim": "Data final no formato AAAA-MM-DD, opcional.",
            "termo": "Termo de busca, opcional. Exemplo: prova, aula, IA.",
        },
    },
    {
        "name": "listar_tarefas",
        "description": "Lista tarefas acadêmicas pendentes ou todas as tarefas.",
        "args": {"incluir_concluidas": "booleano; false para mostrar apenas pendentes."},
    },
    {
        "name": "adicionar_tarefa",
        "description": "Adiciona uma nova tarefa acadêmica.",
        "args": {
            "titulo": "Descrição curta da tarefa.",
            "prazo": "Prazo no formato AAAA-MM-DD, opcional.",
            "disciplina": "Nome da disciplina, opcional.",
            "prioridade": "baixa, média ou alta.",
        },
    },
    {
        "name": "concluir_tarefa",
        "description": "Marca uma tarefa como concluída pelo id ou parte do título.",
        "args": {"tarefa_id_ou_titulo": "id ou trecho do título da tarefa."},
    },
    {
        "name": "buscar_material_rag",
        "description": "Busca informações nos materiais acadêmicos locais usando RAG. Use para verificar se um conceito está nos documentos do aluno. Se o tema não estiver na base, a ferramenta retorna RESULTADO_VAZIO para permitir fallback acadêmico transparente.",
        "args": {
            "pergunta": "Pergunta acadêmica ou conceito que deve ser verificado nos documentos locais.",
            "metodo": "bm25, dense ou hibrido. Padrão: hibrido.",
            "k": "Quantidade de chunks recuperados. Padrão: 3.",
        },
    },
    {
        "name": "gerar_exercicios",
        "description": "Gera exercícios de estudo com base em um tema e nos materiais do RAG.",
        "args": {"tema": "Tema acadêmico.", "quantidade": "Número de exercícios. Padrão: 3."},
    },
    {
        "name": "planejar_estudos",
        "description": "Monta plano de estudos combinando agenda, tarefas e materiais.",
        "args": {
            "objetivo": "Objetivo do estudo. Exemplo: prova de IA.",
            "dias": "Quantidade de dias do plano. Padrão: 3.",
        },
    },
]


class ToolRegistry:
    def __init__(self, rag: RagEngine | None = None) -> None:
        self.agenda = AgendaStore()
        self.tarefas = TarefaStore()
        self.rag = rag or RagEngine(carregar_agora=True)
        self.funcoes: dict[str, Callable[..., Any]] = {
            "consultar_agenda": self.consultar_agenda,
            "listar_tarefas": self.listar_tarefas,
            "adicionar_tarefa": self.adicionar_tarefa,
            "concluir_tarefa": self.concluir_tarefa,
            "buscar_material_rag": self.buscar_material_rag,
            "gerar_exercicios": self.gerar_exercicios,
            "planejar_estudos": self.planejar_estudos,
        }

    def executar(self, nome: str, argumentos: dict[str, Any]) -> Any:
        if nome not in self.funcoes:
            raise ValueError(f"Ferramenta desconhecida: {nome}")
        try:
            saida = self.funcoes[nome](**argumentos)
        except TypeError as exc:
            raise ValueError(f"Argumentos inválidos para {nome}: {argumentos}") from exc
        registrar_tool_call(nome, argumentos, saida)
        return saida

    def consultar_agenda(self, inicio: str | None = None, fim: str | None = None, termo: str | None = None) -> list[dict]:
        return self.agenda.consultar(inicio=inicio, fim=fim, termo=termo)

    def listar_tarefas(self, incluir_concluidas: bool = False) -> list[dict]:
        return self.tarefas.listar(incluir_concluidas=incluir_concluidas)

    def adicionar_tarefa(self, titulo: str, prazo: str = "", disciplina: str = "", prioridade: str = "média") -> dict:
        return self.tarefas.adicionar(Tarefa(titulo=titulo, prazo=prazo, disciplina=disciplina, prioridade=prioridade))

    def concluir_tarefa(self, tarefa_id_ou_titulo: str) -> dict:
        return self.tarefas.concluir(tarefa_id_ou_titulo)

    def buscar_material_rag(self, pergunta: str, metodo: str = "hibrido", k: int = 3) -> dict:
        return self.rag.responder(pergunta=pergunta, metodo=metodo, k=int(k))

    def gerar_exercicios(self, tema: str, quantidade: int = 3) -> dict:
        pergunta = f"Explique os principais conceitos sobre {tema} para criar exercícios."
        resultado = self.rag.responder(pergunta=pergunta, metodo="hibrido", k=3)
        contexto = resultado["resposta"]
        # Geração final fica no Agent, mas retornamos base estruturada para a LLM montar exercícios.
        return {
            "tema": tema,
            "quantidade": int(quantidade),
            "base_para_exercicios": contexto,
            "resultado_vazio": resultado.get("resultado_vazio", False),
            "documentos_recuperados": resultado["documentos_recuperados"],
        }

    def planejar_estudos(self, objetivo: str, dias: int = 3) -> dict:
        hoje = date.today()
        fim = hoje + timedelta(days=int(dias))
        eventos = self.agenda.consultar(inicio=hoje.isoformat(), fim=fim.isoformat())
        tarefas = self.tarefas.listar(incluir_concluidas=False)
        materiais = self.rag.buscar(objetivo, metodo="hibrido", k=3)
        return {
            "objetivo": objetivo,
            "periodo": {"inicio": hoje.isoformat(), "fim": fim.isoformat()},
            "agenda": eventos,
            "tarefas_pendentes": tarefas,
            "materiais_relevantes": materiais,
        }
