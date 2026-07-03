# Issue 5 — Painel "Progresso" (analytics de dificuldades e revisões)

## Parent

`docs/PRD_MELHORIAS.md` — Módulo 5 (Learning analytics) + parte do Módulo 6 (frontend)

## What to build

Novo módulo `src/analytics.py` com a classe `LearningAnalytics(dificuldades_store=None, revisoes_store=None)`, expondo `resumo(dias: int = 30) -> dict`. Não realiza chamadas a LLM ou RAG — opera apenas sobre os dados já persistidos em `DificuldadeStore` e `RevisaoStore`.

`resumo()` retorna:

- `dificuldades_por_topico`: contagem de dificuldades agrupadas por tópico, ordenada de forma decrescente.
- `dificuldades_por_periodo`: contagem de dificuldades agrupadas por dia/semana dentro da janela de `dias`.
- `revisoes`: `{total, avaliadas, taxa_acerto, distribuicao, nota_media}` — `taxa_acerto` é `0` quando `avaliadas == 0` (sem divisão por zero); `distribuicao` agrupa por classificação (ex.: CORRECT/PARTIAL/INCORRECT).
- `temas_recorrentes`: combina tópicos de `dificuldades` com temas de revisões classificadas como PARTIAL/INCORRECT, identificando os temas que mais aparecem.

Novo endpoint `GET /api/analytics/progresso?dias=30` em `web_api/main.py`, que instancia `LearningAnalytics` com os stores existentes e retorna `resumo(dias=...)`.

Frontend: novo item de navegação "Progresso" (ícone `TrendingUp` de `lucide-react`) na sidebar e no menu mobile. Novo componente `ProgressoView` que busca o endpoint e renderiza as três visualizações (dificuldades por tópico, dificuldades por período, revisões/taxa de acerto e temas recorrentes) usando barras CSS reaproveitando classes existentes (`.evidence-pill`, `.list-card`), sem introduzir biblioteca de gráficos. Estado vazio (mensagem amigável) quando não há dificuldades nem revisões.

## Acceptance criteria

- [ ] `LearningAnalytics.resumo()` não realiza chamadas a LLM nem ao `RagEngine`
- [ ] `taxa_acerto` retorna `0` quando `revisoes.avaliadas == 0`, sem levantar exceção de divisão por zero
- [ ] `dificuldades_por_topico` é retornado em ordem decrescente de contagem
- [ ] `temas_recorrentes` combina tópicos de `dificuldades` com temas de revisões PARTIAL/INCORRECT
- [ ] `GET /api/analytics/progresso?dias=30` retorna o formato de `resumo()`, respeitando o parâmetro `dias`
- [ ] Sidebar e menu mobile incluem o item "Progresso" com ícone `TrendingUp`
- [ ] `ProgressoView` renderiza as três visualizações usando o design system existente (sem nova lib de gráficos)
- [ ] Estado vazio é exibido quando não há dificuldades nem revisões registradas
- [ ] Testes cobrem: 0 itens, 1 item, múltiplos itens, e o caso `taxa_acerto` com `avaliadas == 0`

## Blocked by

Nenhum — pode começar imediatamente.
