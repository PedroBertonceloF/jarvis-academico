"""Harness de avaliação da recuperação (RAG) — a "verificação" do loop.

Mede recall@k: para cada pergunta de avaliação, o documento-fonte esperado
aparece entre os k trechos recuperados? O gabarito vem de
docs/AVALIACAO_10_PERGUNTAS.md (fonte primária de cada pergunta).

Não usa a LLM: `RagEngine.buscar()` só faz recuperação, então roda sem token.

Uso (a partir da raiz do projeto):
    # rápido, sem baixar modelos (BM25 puro):
    RAG_MODE=lexical LLM_MODE=mock python scripts/eval_rag.py
    # configuração real (híbrido denso+BM25; baixa o modelo de embeddings):
    LLM_MODE=mock python scripts/eval_rag.py

Env opcionais:
    RAG_EVAL_METHOD=hibrido|dense|bm25   (default: hibrido)
    RAG_EVAL_K=3                         (default: 3)
    RAG_EVAL_MIN=0.9                     (fração mínima de acerto p/ passar; default 0.9)

Sai com código 0 se recall@k >= RAG_EVAL_MIN, senão 1. Esse exit code é o
sinal objetivo de "done" que um loop/CI pode checar.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Permite `from src.rag import ...` ao rodar da raiz do projeto.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.rag import RagEngine  # noqa: E402

# Gabarito: pergunta -> (fonte primária esperada, fontes secundárias desejáveis).
# Extraído de docs/AVALIACAO_10_PERGUNTAS.md.
GOLD: list[tuple[str, str, list[str]]] = [
    ("O que é RAG?", "01_rag.md", []),
    ("Qual a diferença entre BM25 e embeddings?", "02_bm25.md", ["03_embeddings.md"]),
    ("Por que fazer chunking?", "README_DATASET.md", ["01_rag.md"]),
    ("O que é FAISS?", "04_faiss.md", []),
    ("O que é KNN?", "05_knn.md", []),
    ("Por que normalizar atributos no KNN?", "06_normalizacao_knn.md", []),
    ("Para que serve a função sigmoide?", "09_regressao_logistica.md", []),
    ("O que é gradiente descendente?", "07_gradiente_descendente.md", []),
    ("Qual a diferença entre regressão linear e logística?",
     "08_regressao_linear.md", ["09_regressao_logistica.md"]),
    ("O que é tool calling?", "10_tool_calling.md", []),
]


def main() -> int:
    metodo = os.getenv("RAG_EVAL_METHOD", "hibrido").strip().lower()
    k = int(os.getenv("RAG_EVAL_K", "3"))
    minimo = float(os.getenv("RAG_EVAL_MIN", "0.9"))

    engine = RagEngine()
    print(f"modo_recuperacao={engine.modo_recuperacao_atual} | método={metodo} | k={k}\n")

    acertos = 0
    faltando_secundarias = 0
    soma_rr = 0.0  # para MRR

    for i, (pergunta, esperado, tambem) in enumerate(GOLD, start=1):
        docs = engine.buscar(pergunta, metodo=metodo, k=k)
        fontes = [d["fonte"] for d in docs]

        rank = next((j for j, f in enumerate(fontes, start=1) if f == esperado), None)
        ok = rank is not None
        acertos += int(ok)
        soma_rr += (1.0 / rank) if rank else 0.0

        faltou = [f for f in tambem if f not in fontes]
        faltando_secundarias += int(bool(faltou))

        marca = "OK " if ok else "XX "
        extra = f"  (falta secundária: {', '.join(faltou)})" if faltou else ""
        print(f"{marca}{i:2d}. {pergunta}")
        print(f"       esperado={esperado} rank={rank} top{k}={fontes}{extra}")

    n = len(GOLD)
    recall = acertos / n
    mrr = soma_rr / n
    print(f"\nrecall@{k} = {acertos}/{n} = {recall:.2f} | MRR = {mrr:.3f} | "
          f"secundárias faltando = {faltando_secundarias}")
    print(f"meta: recall@{k} >= {minimo:.2f} -> {'PASSOU' if recall >= minimo else 'FALHOU'}")

    return 0 if recall >= minimo else 1


if __name__ == "__main__":
    raise SystemExit(main())
