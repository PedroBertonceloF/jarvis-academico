from __future__ import annotations

import csv
from pathlib import Path

from src.rag import RagEngine

PERGUNTAS = [
    "O que é RAG?",
    "Qual a diferença entre BM25 e embeddings?",
    "Por que fazer chunking?",
    "O que é FAISS?",
    "O que é KNN?",
    "Por que normalizar atributos no KNN?",
    "Para que serve a função sigmoide?",
    "O que é gradiente descendente?",
    "Qual a diferença entre regressão linear e logística?",
    "O que é tool calling?",
]


def main() -> None:
    rag = RagEngine(carregar_agora=True)
    saida = Path("avaliacao_sistema.csv")
    with saida.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["pergunta", "documentos_recuperados", "resposta", "classificacao", "observacao"],
        )
        writer.writeheader()
        for pergunta in PERGUNTAS:
            resultado = rag.responder(pergunta, metodo="hibrido", k=3)
            docs = "; ".join([f"{d['id']} ({d['fonte']}, score={d['score']})" for d in resultado["documentos_recuperados"]])
            writer.writerow({
                "pergunta": pergunta,
                "documentos_recuperados": docs,
                "resposta": resultado["resposta"],
                "classificacao": "PREENCHER: correta/parcialmente correta/incorreta",
                "observacao": "PREENCHER após análise humana",
            })
    print(f"Arquivo gerado: {saida.resolve()}")


if __name__ == "__main__":
    main()
