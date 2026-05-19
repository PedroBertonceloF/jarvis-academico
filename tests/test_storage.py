from src.storage import Tarefa, TarefaStore


def test_tarefa_cria_id():
    tarefa = Tarefa(titulo="Estudar RAG")
    assert tarefa.id
    assert tarefa.concluida is False
