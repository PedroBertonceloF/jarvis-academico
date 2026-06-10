# Checklist Trabalho 2 — JARVIS Acadêmico

Este checklist consolida a segunda parte da implementação e aponta onde cada requisito aparece no projeto.

## Escopo da segunda etapa

Na divisão do trabalho, o Trabalho 2 cobre principalmente:

- funcionalidade 3.4: planejamento de estudos;
- melhorias de aprendizado;
- avaliação do sistema;
- análise de erros;
- evidências de dataset, engenharia, integração com LLM e tool calling.

## Requisitos e evidências

| Requisito | Status | Evidência no projeto |
|---|---|---|
| Planejamento de estudos | Atendido | `src/tools.py` implementa `planejar_estudos`, combinando agenda, tarefas, dificuldades e materiais RAG. |
| Tool calling com no mínimo 5 ferramentas | Atendido | `TOOL_SPECS` possui agenda, tarefas, RAG, exercícios, revisão ativa, dificuldades e plano de estudos. |
| Decisão de ferramenta pela LLM | Atendido | `src/agent.py` pede JSON de decisão para a LLM antes de executar ferramentas. |
| Consulta a materiais com RAG | Atendido | `src/rag.py` faz chunking, BM25, modo híbrido, fontes, scores e diagnóstico de relevância. |
| Fallback quando não há evidência | Atendido | `RagEngine.responder` retorna `resultado_vazio`; `src/agent.py` obriga aviso explícito ao aluno. |
| Agenda acadêmica | Atendido | `AgendaStore`, endpoints `/api/agenda` e ferramentas `consultar_agenda`/`adicionar_evento`. |
| Lista de tarefas | Atendido | `TarefaStore`, endpoints `/api/tasks` e ferramentas `listar_tarefas`/`adicionar_tarefa`/`concluir_tarefa`. |
| Melhoria de aprendizado | Atendido | `src/learning.py` gera revisão ativa, avalia respostas e registra dificuldades. |
| Geração de exercícios | Atendido | Ferramenta `gerar_exercicios` usa o RAG como base para criar prática. |
| Identificação de dificuldades | Atendido | Ferramentas `registrar_dificuldade` e `listar_dificuldades`; avaliação de revisão registra dificuldades automaticamente. |
| Avaliação com 10 perguntas | Documentado | `docs/AVALIACAO_10_PERGUNTAS.md`. |
| Análise de erros com pelo menos 3 falhas | Atendido | `docs/ANALISE_DE_ERROS.md` registra falhas, causas, correções e resultados. |
| Dataset próprio com pelo menos 10 documentos | Atendido | `data/` contém 10 arquivos base; `data/README_DATASET.md` descreve origem, tipo e limitações. |
| Chunking explicado | Atendido | `README.md`, `data/README_DATASET.md` e `src/rag.py`. |
| Logs/evidências técnicas | Atendido | `src/logger.py`, `/api/logs` e aba "Evidências" no frontend. |
| Tratamento de erros | Atendido | Fallback acadêmico, timeout, autenticação, erro HTTP da LLM e diagnóstico seguro. |
| Segurança de secrets | Atendido | `.env` não versionado; `.env.example` usa placeholder; documentação orienta Secrets do Hugging Face. |
| Deploy Hugging Face | Atendido se Space estiver online | `Dockerfile`, README com YAML do Space e `app_port: 7860`. |
| Integração com LLM | Atendido localmente quando `/api/debug/gemma-ping` retorna `ok=true` | `src/llm_client.py`; endpoint legado `/api/debug/gemma-ping`. |

## Observação sobre nomes legados da LLM

O projeto mantém `LLM_MODE=gemma`, `GEMMA_BASE_URL`, `GEMMA_MODEL` e `GEMMA_API_KEY` por compatibilidade com versões anteriores e com o Space já configurado. No endpoint atual fornecido para a entrega, esses campos apontam para:

```env
GEMMA_BASE_URL=https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq
GEMMA_MODEL=Qwen/Qwen2.5-14B-Instruct-AWQ
```

O código também aceita `LLM_MODE=qwen`, `LLM_MODE=remote` e `LLM_MODE=openai_compatible`, mas `LLM_MODE=gemma` continua funcionando para não quebrar o deploy.

## Pontos para demonstrar no vídeo

1. Abrir `/api/status` e mostrar modelo, RAG, documentos e chunks.
2. Abrir `/api/debug/gemma-ping` e mostrar `ok=true` sem expor chave.
3. Perguntar "O que é RAG?" e mostrar fontes/scores.
4. Perguntar "O que é heap?" e mostrar fallback acadêmico.
5. Montar um plano de estudos para provar a ferramenta `planejar_estudos`.
6. Gerar exercícios sobre embeddings.
7. Iniciar revisão ativa sobre RAG.
8. Registrar dificuldade em BM25 e listar dificuldades.
9. Mostrar a aba Evidências com tool calls, entrada, saída e JSON bruto.
10. Mostrar `docs/AVALIACAO_10_PERGUNTAS.md` e `docs/ANALISE_DE_ERROS.md`.
