# Issue 1 — Storage confiável (escrita atômica + validação)

## Parent

`docs/PRD_MELHORIAS.md` — Módulo 1 (Storage reliability layer)

## What to build

Substituir as funções soltas `_read_json`/`_write_json` em `src/storage.py` por uma classe `JsonCollectionStore(path)` com `ler() -> list[dict]` e `escrever(itens: list[dict]) -> None`.

`escrever()` deve ser atômico: serializa para um arquivo temporário no mesmo diretório e usa `os.replace()` para substituir o arquivo final, evitando arquivos truncados em caso de falha no meio da escrita. Lock baseado em criação exclusiva de arquivo (`open(..., "x")`) com retry curto — sem novas dependências, suficiente para a instância única do Hugging Face Spaces.

`AgendaStore`, `TarefaStore`, `DificuldadeStore` e `RevisaoStore` passam a compor uma instância de `JsonCollectionStore` em vez de chamar as funções de módulo diretamente.

Validação adicionada nos pontos de escrita (não no `JsonCollectionStore`, que permanece agnóstico de schema):

- `AgendaStore.adicionar` / `TarefaStore.adicionar`: campos de data (`data`, `prazo`) devem ser `AAAA-MM-DD` ou string vazia; valor inválido levanta `ValueError`.
- `TarefaStore.adicionar`: `prioridade` deve estar em `{"baixa", "média", "alta"}`.

Em `web_api/main.py`, o `ValueError` desses validadores deve ser convertido em `HTTPException(422)` com a mensagem original nos endpoints `POST /api/tasks` e `POST /api/agenda` (em vez de cair no handler genérico 500).

## Acceptance criteria

- [x] `JsonCollectionStore.escrever()` grava via arquivo temporário + `os.replace()`, sem deixar arquivos temporários após sucesso
- [x] `AgendaStore`, `TarefaStore`, `DificuldadeStore` e `RevisaoStore` usam `JsonCollectionStore` para leitura/escrita
- [x] `AgendaStore.adicionar`/`TarefaStore.adicionar` rejeitam datas que não sejam `AAAA-MM-DD` nem string vazia, levantando `ValueError`
- [x] `TarefaStore.adicionar` rejeita `prioridade` fora de `{"baixa", "média", "alta"}`
- [x] `POST /api/tasks` e `POST /api/agenda` retornam `422` com a mensagem do validador para entradas inválidas
- [x] Requisições válidas existentes continuam funcionando sem alteração de comportamento
- [x] Testes cobrem: round-trip de leitura/escrita, rejeição de data inválida, rejeição de prioridade inválida
- [x] Funciona com `RAG_MODE=lexical` e `LLM_MODE=mock` (sem dependência de RAG/LLM)

## Blocked by

Nenhum — pode começar imediatamente.
