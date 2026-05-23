from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag import carregar_documentos, chunk_texto


def main() -> None:
    docs = carregar_documentos()
    print(f"Documentos encontrados: {len(docs)}")

    for doc in docs:
        chunks = chunk_texto(doc["texto"])
        print(
            f"- {doc['fonte']} | "
            f"tipo={doc['tipo']} | "
            f"chars={len(doc['texto'])} | "
            f"chunks={len(chunks)}"
        )

    if len(docs) < 10:
        raise SystemExit("Dataset insuficiente: inclua pelo menos 10 documentos em /data.")

    print("Dataset OK: mínimo de 10 documentos atendido.")


if __name__ == "__main__":
    main()
