# Issue 2 — `/api/health` com diagnóstico real (RAG, LLM, storage)

## Parent

`docs/PRD_MELHORIAS.md` — Módulo 2 (Health aggregator)

## What to build

Criar `src/health.py` com `verificar_saude(rag: RagEngine | None = None, verbose: bool = False) -> dict`.

Sem chamada à LLM por padrão. Retorna:

- `rag`: `{documentos, chunks, modo_recuperacao}` (reaproveita `RagEngine`/`_resumo_base`).
- `llm`: `{modo, configurado}` — `configurado` é `True` se `settings.usando_mock` ou se `settings.validate_llm()` não levanta exceção (sem chamar a rede).
- `storage`: `{ok: bool, erro: str | None}` — escreve, lê e remove um arquivo `_healthcheck.tmp` em `settings.storage_dir`.
- `ok`: `True` somente se `rag`, `llm.configurado` e `storage.ok` forem todos saudáveis. RAG vazio (sem documentos) é um estado válido e não deve, por si só, tornar `ok=False`.

Quando `verbose=True` (via `/api/health?verbose=true`), adicionar um campo `llm_ping` reaproveitando a lógica de `GemmaClient().ping()` já usada por `/api/debug/gemma-ping`.

`web_api/main.py`: `/api/health` passa a chamar `verificar_saude()`, mantendo todos os campos hoje existentes (`ok`, `modo_llm`, `llm_provider`, etc.) e adicionando os novos campos de forma aditiva.

## Acceptance criteria

- [ ] `verificar_saude()` retorna as chaves `rag`, `llm`, `storage`, `ok` sem chamar a LLM remota por padrão
- [ ] A checagem de storage faz escrita+leitura+remoção de um arquivo temporário em `storage_dir` e reporta `ok=False` com `erro` em caso de falha
- [ ] `llm.configurado` é `True` quando `usando_mock` ou quando `settings.validate_llm()` não levanta exceção
- [ ] `/api/health` inclui os novos campos de forma aditiva; campos existentes (`ok`, `modo_llm`, `llm_provider`, etc.) permanecem inalterados
- [ ] `/api/health?verbose=true` inclui `llm_ping` usando a lógica existente de `GemmaClient().ping()`
- [ ] Funciona com `LLM_MODE=mock` e `RAG_MODE=lexical`, sem exigir token configurado
- [ ] Testes cobrem: modo mock retorna `ok=True` com o formato esperado; RAG vazio (sem documentos) reflete em `rag.modo_recuperacao` sem forçar `ok=False`

## Blocked by

Nenhum — pode começar imediatamente.
