# Issue 4 — Citações inline no chat (fontes + score abaixo da resposta)

## Parent

`docs/PRD_MELHORIAS.md` — Módulo 4 (Citation extraction) + parte do Módulo 6 (frontend)

## What to build

Nova função pura `extrair_fontes_citadas(resultados: list[dict]) -> list[dict]`, em `src/agent.py` (próxima ao `_responder_final`, mesmo padrão de funções utilitárias já presente no módulo).

Percorre `resultados` (a lista `tool_calls`), procura `documentos_recuperados` e `materiais_relevantes` em cada `saida`, e retorna uma lista deduplicada (por `id`, fallback `fonte+score`) de `{"fonte": str, "id": str, "score": float}`, ordenada por `score` decrescente.

`JarvisAgent.responder()` passa a incluir `"fontes_citadas": extrair_fontes_citadas(resultados)` no dicionário retornado, ao lado de `resposta` e `tool_calls`. Lista vazia quando não há fontes (ex.: conversa casual, fallback acadêmico sem RAG).

`web_api/main.py` (`/api/chat`): repassa `fontes_citadas` sem alteração — o endpoint já retorna o dicionário do agente diretamente.

Frontend (`MessageBubble`): renderizar `message.fontes_citadas` como uma linha de chips abaixo do conteúdo markdown da mensagem do assistente, reaproveitando o estilo `.source-chip` e o `formatScore` já usados em `ContextPanel`/`extractSources`. Quando `fontes_citadas` é vazio ou ausente, nada é renderizado (sem espaço extra).

## Acceptance criteria

- [ ] `extrair_fontes_citadas([])` retorna `[]`
- [ ] `extrair_fontes_citadas` deduplica fontes por `id` (fallback `fonte+score`) entre múltiplos `tool_calls`
- [ ] `extrair_fontes_citadas` ordena o resultado por `score` decrescente
- [ ] `JarvisAgent.responder()` sempre inclui a chave `"fontes_citadas"` (lista, possivelmente vazia)
- [ ] `/api/chat` retorna `fontes_citadas` sem alteração em relação à saída do agente
- [ ] Mensagens do assistente com `fontes_citadas` não vazio mostram chips com nome da fonte + score abaixo da mensagem
- [ ] Mensagens com `fontes_citadas` vazio/ausente renderizam sem espaço extra ou chip vazio
- [ ] Testes cobrem: lista vazia, um único `tool_call`, múltiplos `tool_calls` com fontes duplicadas

## Blocked by

Nenhum — pode começar imediatamente.
