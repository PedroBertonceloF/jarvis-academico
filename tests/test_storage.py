import pytest

from src.storage import (
    AgendaStore,
    EventoAgenda,
    JsonCollectionStore,
    Tarefa,
    TarefaStore,
)


def test_tarefa_cria_id():
    tarefa = Tarefa(titulo="Estudar RAG")
    assert tarefa.id
    assert tarefa.concluida is False


def test_json_collection_store_round_trip(tmp_path):
    store = JsonCollectionStore(tmp_path / "itens.json")

    assert store.ler() == []

    itens = [{"id": "1", "valor": "a"}, {"id": "2", "valor": "b"}]
    store.escrever(itens)

    assert store.ler() == itens


def test_json_collection_store_nao_deixa_arquivo_temporario(tmp_path):
    path = tmp_path / "itens.json"
    store = JsonCollectionStore(path)

    store.escrever([{"id": "1"}])

    arquivos = list(tmp_path.iterdir())
    assert arquivos == [path]


def test_tarefa_store_rejeita_prazo_invalido(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.TAREFAS_PATH", tmp_path / "tarefas.json")
    store = TarefaStore()

    with pytest.raises(ValueError):
        store.adicionar(Tarefa(titulo="Estudar", prazo="11/06/2026"))


def test_tarefa_store_rejeita_prioridade_invalida(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.TAREFAS_PATH", tmp_path / "tarefas.json")
    store = TarefaStore()

    with pytest.raises(ValueError):
        store.adicionar(Tarefa(titulo="Estudar", prioridade="urgente"))


def test_tarefa_store_aceita_prazo_vazio_e_prioridade_valida(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.TAREFAS_PATH", tmp_path / "tarefas.json")
    store = TarefaStore()

    item = store.adicionar(Tarefa(titulo="Estudar", prazo="", prioridade="alta"))

    assert item["prazo"] == ""
    assert store.listar() == [item]


def test_agenda_store_rejeita_data_invalida(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.AGENDA_PATH", tmp_path / "agenda.json")
    store = AgendaStore()

    with pytest.raises(ValueError):
        store.adicionar(EventoAgenda(data="2026-13-40", titulo="Aula"))


def test_agenda_store_aceita_data_valida(tmp_path, monkeypatch):
    monkeypatch.setattr("src.storage.AGENDA_PATH", tmp_path / "agenda.json")
    store = AgendaStore()

    item = store.adicionar(EventoAgenda(data="2026-06-11", titulo="Aula"))

    assert item["data"] == "2026-06-11"
    assert store.listar() == [item]
