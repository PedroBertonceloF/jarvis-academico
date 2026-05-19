from __future__ import annotations

from src.rag import carregar_documentos, chunk_texto


def main() -> None:
    docs = carregar_documentos()
    print(f"Documentos encontrados: {len(docs)}")
    for doc in docs:
        chunks = chunk_texto(doc["texto"])
        print(f"- {doc['fonte']} | tipo={doc['tipo']} | chars={len(doc['texto'])} | chunks={len(chunks)}")
    if len(docs) < 10:
        raise SystemExit("Dataset insuficiente: inclua pelo menos 10 documentos em /data.")
    print("Dataset OK: mínimo de 10 documentos atendido.")


if __name__ == "__main__":
    main()
