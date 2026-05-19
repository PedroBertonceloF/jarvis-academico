from src.rag import chunk_texto


def test_chunking_retorna_partes():
    texto = "Parágrafo um.\n\n" + "A" * 1200
    chunks = chunk_texto(texto, tamanho=300, sobreposicao=50)
    assert len(chunks) >= 2
    assert all(len(c) <= 350 for c in chunks)
