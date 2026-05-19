import json

from src.logger import registrar_tool_call, LOG_PATH


def test_logger_registra_jsonl(tmp_path, monkeypatch):
    # Redireciona o caminho do log apenas neste teste.
    import src.logger as logger
    monkeypatch.setattr(logger, "LOG_PATH", tmp_path / "tool_calls.jsonl")

    registrar_tool_call("teste", {"entrada": 1}, {"saida": 2})
    linha = logger.LOG_PATH.read_text(encoding="utf-8").strip()
    registro = json.loads(linha)
    assert registro["ferramenta"] == "teste"
    assert registro["entrada"] == {"entrada": 1}
    assert registro["saida"] == {"saida": 2}
