from src.rag import RagEngine


def test_resultado_vazio_quando_nao_ha_termo_relevante_no_contexto():
    rag = RagEngine(carregar_agora=False)
    docs = [{"texto": "RAG usa documentos, embeddings e recuperação híbrida."}]

    diagnostico = rag._diagnosticar_relevancia("O que é heap?", docs)

    assert diagnostico["qtd_termos_encontrados"] == 0
    assert rag._resultado_vazio(diagnostico) is True


def test_nao_vazio_quando_ha_termo_relevante_no_contexto():
    rag = RagEngine(carregar_agora=False)
    docs = [{"texto": "Regressão logística usa a função sigmoide para classificação binária."}]

    diagnostico = rag._diagnosticar_relevancia("Explique regressão logística", docs)

    assert "regressão" in diagnostico["termos_encontrados_no_contexto"]
    assert rag._resultado_vazio(diagnostico) is False
