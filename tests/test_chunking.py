import src.rag as rag_module
from src.rag import RagEngine, chunk_texto


def test_chunking_retorna_partes():
    texto = "Parágrafo um.\n\n" + "A" * 1200
    chunks = chunk_texto(texto, tamanho=300, sobreposicao=50)
    assert len(chunks) >= 2
    assert all(len(c) <= 350 for c in chunks)


def test_rag_faz_fallback_lexical_quando_busca_densa_indisponivel(monkeypatch):
    monkeypatch.setattr(
        rag_module,
        "carregar_documentos",
        lambda: [{"id": "doc", "fonte": "doc.md", "texto": "RAG usa recuperação e geração."}],
    )
    monkeypatch.setattr(rag_module, "modo_rag_lexical", lambda: False)

    def falhar_carregamento_dense():
        raise ModuleNotFoundError("sentence_transformers")

    monkeypatch.setattr(rag_module, "_carregar_sentence_transformer", falhar_carregamento_dense)

    engine = RagEngine(carregar_agora=True)

    assert engine.modo_recuperacao_atual == "lexical_bm25_fallback"
    assert engine.buscar("O que é RAG?", metodo="hibrido", k=1)
