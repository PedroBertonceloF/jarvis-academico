from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Iterable

import faiss
import numpy as np
from pypdf import PdfReader
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from .config import settings
from .llm_client import GemmaClient

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".py"}


def tokenizar(texto: str) -> list[str]:
    return re.findall(r"\w+", texto.lower())


def normalizar(v: np.ndarray) -> np.ndarray:
    v = np.array(v, dtype="float32")
    delta = float(v.max() - v.min()) if len(v) else 0.0
    if delta < 1e-9:
        return np.zeros_like(v)
    return (v - v.min()) / delta


def ler_arquivo(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".txt", ".md", ".py"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if ext == ".pdf":
        reader = PdfReader(str(path))
        partes = []
        for idx, page in enumerate(reader.pages, start=1):
            texto = page.extract_text() or ""
            if texto.strip():
                partes.append(f"\n\n[Página {idx}]\n{texto}")
        return "\n".join(partes)
    return ""


def carregar_documentos(data_dir: Path = settings.data_dir) -> list[dict]:
    docs: list[dict] = []
    for path in sorted(data_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            texto = ler_arquivo(path).strip()
            if texto:
                docs.append({
                    "id": path.stem,
                    "fonte": str(path.relative_to(settings.data_dir)),
                    "texto": texto,
                    "tipo": path.suffix.lower().replace(".", ""),
                })
    return docs


def chunk_texto(texto: str, tamanho: int = 700, sobreposicao: int = 80) -> list[str]:
    if sobreposicao >= tamanho:
        raise ValueError("A sobreposição deve ser menor que o tamanho do chunk.")

    texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
    paragrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    chunks: list[str] = []
    atual = ""

    for paragrafo in paragrafos:
        if len(atual) + len(paragrafo) + 2 <= tamanho:
            atual = (atual + "\n\n" + paragrafo).strip()
        else:
            if atual:
                chunks.append(atual)
            if len(paragrafo) <= tamanho:
                atual = paragrafo
            else:
                passo = tamanho - sobreposicao
                for inicio in range(0, len(paragrafo), passo):
                    parte = paragrafo[inicio:inicio + tamanho].strip()
                    if parte:
                        chunks.append(parte)
                atual = ""
    if atual:
        chunks.append(atual)
    return chunks


@dataclass
class RagConfig:
    tamanho_chunk: int = 700
    sobreposicao: int = 80
    alpha_hibrido: float = 0.6


class RagEngine:
    def __init__(self, config: RagConfig | None = None, carregar_agora: bool = True) -> None:
        self.config = config or RagConfig()
        self.docs: list[dict] = []
        self.chunks: list[dict] = []
        self.modelo_embed: SentenceTransformer | None = None
        self.matriz_emb: np.ndarray | None = None
        self.indice_faiss = None
        self.indice_bm25 = None
        if carregar_agora:
            self.reindexar()

    def reindexar(self) -> dict:
        self.docs = carregar_documentos()
        self.chunks = []
        for doc in self.docs:
            partes = chunk_texto(
                doc["texto"],
                tamanho=self.config.tamanho_chunk,
                sobreposicao=self.config.sobreposicao,
            )
            for i, parte in enumerate(partes):
                self.chunks.append({
                    "id": f"{doc['id']}_chunk_{i:04d}",
                    "doc_id": doc["id"],
                    "fonte": doc["fonte"],
                    "texto": parte,
                })

        if not self.chunks:
            self.indice_bm25 = None
            self.indice_faiss = None
            self.matriz_emb = None
            return {"documentos": 0, "chunks": 0}

        corpus_tokenizado = [tokenizar(c["texto"]) for c in self.chunks]
        self.indice_bm25 = BM25Okapi(corpus_tokenizado)

        self.modelo_embed = SentenceTransformer(settings.embedding_model)
        textos = [c["texto"] for c in self.chunks]
        self.matriz_emb = self.modelo_embed.encode(
            textos,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype("float32")

        self.indice_faiss = faiss.IndexFlatIP(self.matriz_emb.shape[1])
        self.indice_faiss.add(self.matriz_emb)
        return {"documentos": len(self.docs), "chunks": len(self.chunks)}

    def _garantir_indice(self) -> None:
        if not self.chunks or self.indice_bm25 is None or self.indice_faiss is None:
            raise RuntimeError("Índice RAG vazio. Coloque documentos na pasta /data e rode reindexar().")

    def recuperar_bm25(self, pergunta: str, k: int = 3) -> list[dict]:
        self._garantir_indice()
        scores = self.indice_bm25.get_scores(tokenizar(pergunta))
        idx = np.argsort(scores)[::-1][:k]
        return [self._formatar_resultado(i, float(scores[i])) for i in idx]

    def recuperar_dense(self, pergunta: str, k: int = 3) -> list[dict]:
        self._garantir_indice()
        q = self.modelo_embed.encode([pergunta], normalize_embeddings=True).astype("float32")
        scores, idx = self.indice_faiss.search(q, min(k, len(self.chunks)))
        return [self._formatar_resultado(int(i), float(scores[0][j])) for j, i in enumerate(idx[0]) if i >= 0]

    def recuperar_hibrido(self, pergunta: str, k: int = 3, alpha: float | None = None) -> list[dict]:
        self._garantir_indice()
        alpha = self.config.alpha_hibrido if alpha is None else alpha
        score_bm25 = np.array(self.indice_bm25.get_scores(tokenizar(pergunta)), dtype="float32")
        q = self.modelo_embed.encode([pergunta], normalize_embeddings=True).astype("float32")
        score_dense = np.dot(self.matriz_emb, q[0])
        score_final = alpha * normalizar(score_dense) + (1.0 - alpha) * normalizar(score_bm25)
        idx = np.argsort(score_final)[::-1][:k]
        return [self._formatar_resultado(int(i), float(score_final[i])) for i in idx]

    def _formatar_resultado(self, idx: int, score: float) -> dict:
        item = self.chunks[idx]
        return {
            "id": item["id"],
            "fonte": item["fonte"],
            "score": round(score, 4),
            "texto": item["texto"],
        }

    def buscar(self, pergunta: str, metodo: str = "hibrido", k: int = 3) -> list[dict]:
        metodo = metodo.lower().strip()
        if metodo == "bm25":
            return self.recuperar_bm25(pergunta, k=k)
        if metodo == "dense":
            return self.recuperar_dense(pergunta, k=k)
        return self.recuperar_hibrido(pergunta, k=k)

    def responder(self, pergunta: str, metodo: str = "hibrido", k: int = 3) -> dict:
        docs = self.buscar(pergunta, metodo=metodo, k=k)
        contexto = "\n\n".join(
            f"Trecho {i+1} | Fonte: {d['fonte']} | ID: {d['id']}\n{d['texto']}"
            for i, d in enumerate(docs)
        )
        prompt = (
            "Você é o JARVIS Acadêmico. Responda em português, de forma didática e objetiva.\n"
            "Use apenas o contexto recuperado. Se a resposta não estiver no contexto, diga claramente "
            "que não encontrou evidência suficiente.\n\n"
            f"Contexto:\n{contexto}\n\nPergunta: {pergunta}"
        )
        llm = GemmaClient()
        resposta = llm.chat([
            {"role": "system", "content": "Você responde perguntas acadêmicas com base em evidências recuperadas."},
            {"role": "user", "content": prompt},
        ])
        return {"resposta": resposta, "documentos_recuperados": docs}
