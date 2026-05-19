# Análise de erros

## Falha 1 — Plano de estudos genérico
- **Tipo:** geração.
- **Causa provável:** a ferramenta retorna dados corretos, mas o prompt final pode não exigir uma divisão objetiva por dia.
- **Possível solução:** melhorar o prompt de `planejar_estudos` para obrigar saída em formato de cronograma diário com prioridades.

## Falha 2 — Recuperação de temas próximos
- **Tipo:** recuperação.
- **Causa provável:** regressão linear, regressão logística e gradiente descendente possuem termos semanticamente próximos, então o RAG pode recuperar documentos relacionados além do documento principal.
- **Possível solução:** usar metadados por disciplina/tema, ajustar `k`, melhorar chunking ou aplicar reranking.

## Falha 3 — Perguntas ambíguas
- **Tipo:** ambiguidade.
- **Causa provável:** perguntas como “o que devo estudar?” não informam prova, disciplina ou prazo.
- **Possível solução:** o agente deve pedir esclarecimento antes de montar o plano ou inferir prioridade com base na agenda e tarefas.

## Falha 4 — Consumo de tokens
- **Tipo:** engenharia/custo.
- **Causa provável:** enviar muitos chunks ou respostas longas para a LLM aumenta o consumo da API compartilhada.
- **Possível solução:** usar `LLM_MODE=mock` no desenvolvimento, `k=3` no RAG e `max_tokens` reduzido na Gemma.
