from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path
import json
import uuid

from .config import settings

AGENDA_PATH = settings.storage_dir / "agenda.json"
TAREFAS_PATH = settings.storage_dir / "tarefas.json"


def _read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@dataclass
class EventoAgenda:
    data: str
    titulo: str
    hora_inicio: str = ""
    hora_fim: str = ""
    tipo: str = "aula"
    observacao: str = ""


@dataclass
class Tarefa:
    titulo: str
    prazo: str = ""
    disciplina: str = ""
    prioridade: str = "média"
    concluida: bool = False
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


class AgendaStore:
    def listar(self) -> list[dict]:
        return _read_json(AGENDA_PATH, [])

    def salvar_eventos(self, eventos: list[dict]) -> None:
        _write_json(AGENDA_PATH, eventos)

    def adicionar(self, evento: EventoAgenda) -> dict:
        eventos = self.listar()
        item = asdict(evento)
        eventos.append(item)
        eventos.sort(key=lambda x: (x.get("data", ""), x.get("hora_inicio", "")))
        self.salvar_eventos(eventos)
        return item

    def consultar(self, inicio: str | None = None, fim: str | None = None, termo: str | None = None) -> list[dict]:
        eventos = self.listar()
        if inicio:
            eventos = [e for e in eventos if e.get("data", "") >= inicio]
        if fim:
            eventos = [e for e in eventos if e.get("data", "") <= fim]
        if termo:
            termo_low = termo.lower()
            eventos = [
                e for e in eventos
                if termo_low in json.dumps(e, ensure_ascii=False).lower()
            ]
        return eventos


class TarefaStore:
    def listar(self, incluir_concluidas: bool = True) -> list[dict]:
        tarefas = _read_json(TAREFAS_PATH, [])
        if not incluir_concluidas:
            tarefas = [t for t in tarefas if not t.get("concluida", False)]
        return tarefas

    def salvar_tarefas(self, tarefas: list[dict]) -> None:
        _write_json(TAREFAS_PATH, tarefas)

    def adicionar(self, tarefa: Tarefa) -> dict:
        tarefas = self.listar()
        item = asdict(tarefa)
        tarefas.append(item)
        self.salvar_tarefas(tarefas)
        return item

    def concluir(self, tarefa_id_ou_titulo: str) -> dict:
        tarefas = self.listar()
        alvo = tarefa_id_ou_titulo.strip().lower()
        for tarefa in tarefas:
            if tarefa.get("id", "").lower() == alvo or alvo in tarefa.get("titulo", "").lower():
                tarefa["concluida"] = True
                self.salvar_tarefas(tarefas)
                return tarefa
        raise ValueError(f"Tarefa não encontrada: {tarefa_id_ou_titulo}")


def inicializar_dados_demo() -> None:
    agenda = AgendaStore()
    tarefas = TarefaStore()

    if not AGENDA_PATH.exists():
        agenda.salvar_eventos([
            {
                "data": "2026-05-11",
                "hora_inicio": "19:00",
                "hora_fim": "21:00",
                "titulo": "Estudo de RAG e embeddings",
                "tipo": "estudo",
                "observacao": "Revisar chunking, BM25, FAISS e prompt de RAG.",
            },
            {
                "data": "2026-05-12",
                "hora_inicio": "20:00",
                "hora_fim": "21:30",
                "titulo": "Revisão de regressão logística",
                "tipo": "estudo",
                "observacao": "Foco em função sigmoide e gradiente.",
            },
        ])

    if not TAREFAS_PATH.exists():
        tarefas.salvar_tarefas([
            asdict(Tarefa(
                titulo="Montar dataset com 10 documentos acadêmicos",
                prazo="2026-05-18",
                disciplina="Inteligência Artificial",
                prioridade="alta",
            )),
            asdict(Tarefa(
                titulo="Avaliar o sistema com 10 perguntas",
                prazo="2026-05-25",
                disciplina="Inteligência Artificial",
                prioridade="alta",
            )),
        ])
