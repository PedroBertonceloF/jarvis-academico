# Issue 3 — PDF corrompido não derruba o RAG + aviso na UI

## Parent

`docs/PRD_MELHORIAS.md` — Módulo 3 (RAG ingestion error handling)

## What to build

`ler_arquivo` (em `src/rag.py`) passa a capturar exceções genéricas ao processar PDFs (`PdfReader`/extração de página) e retornar string vazia em caso de falha, sem propagar a exceção.

`carregar_documentos` coleta as falhas em uma lista `documentos_com_erro: list[dict]` no formato `{"arquivo": <caminho relativo>, "erro": <mensagem>}`, retornada junto com os documentos válidos. Os demais documentos válidos continuam sendo carregados normalmente.

`RagEngine.reindexar` armazena essa lista em `self.documentos_com_erro` e a inclui no dicionário de retorno.

`web_api/main.py` (`_resumo_base`): inclui `documentos_com_erro` no resumo, exposto em `/api/status` (lista vazia quando não há erros).

Frontend (`MaterialsView`): quando `status.base_rag.documentos_com_erro` (ou equivalente) não estiver vazio, exibir um aviso visível listando os arquivos com erro de leitura. Nada é exibido quando a lista está vazia.

## Acceptance criteria

- [ ] Um PDF corrompido/inválido em `data/` não levanta exceção durante `carregar_documentos`/`reindexar`
- [ ] Outros documentos válidos em `data/` continuam sendo indexados normalmente quando um PDF falha
- [ ] `documentos_com_erro` contém `{"arquivo", "erro"}` para cada arquivo que falhou
- [ ] `/api/status` inclui `documentos_com_erro` (lista vazia quando não há erros)
- [ ] `MaterialsView` exibe um aviso visível listando os arquivos em `documentos_com_erro`, quando não vazio
- [ ] Nenhum aviso é exibido quando `documentos_com_erro` está vazio
- [ ] Testes cobrem: fixture com PDF corrompido, confirmando que `documentos_com_erro` é populado e os demais documentos continuam carregados

## Blocked by

Nenhum — pode começar imediatamente.
