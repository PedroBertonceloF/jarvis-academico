# Arquitetura — JARVIS Acadêmico

## Visão geral

```text
Usuário
  ↓
Interface Streamlit / CLI
  ↓
JarvisAgent
  ↓
GemmaClient decide ferramentas
  ↓
ToolRegistry executa ferramentas
  ├── Agenda JSON
  ├── Tarefas JSON
  ├── RAG: documentos → chunks → BM25 + embeddings + FAISS
  └── Planejamento / exercícios
  ↓
Logger registra entrada e saída
  ↓
Resposta final ao usuário
```

## Módulos principais

- `src/config.py`: carrega variáveis de ambiente e caminhos do projeto.
- `src/llm_client.py`: encapsula acesso à Gemma e modo mock.
- `src/rag.py`: carrega documentos, faz chunking, cria índices BM25/FAISS e responde perguntas.
- `src/tools.py`: define e executa ferramentas disponíveis para o agente.
- `src/agent.py`: usa a LLM para decidir tool calling e montar a resposta final.
- `src/storage.py`: gerencia agenda e tarefas em JSON.
- `src/logger.py`: registra chamadas de ferramentas em `logs/tool_calls.jsonl`.
- `app.py`: interface Streamlit.
- `main.py`: interface por terminal.

## Decisões de arquitetura
O projeto usa módulos profundos com interfaces simples. O agente não precisa conhecer detalhes internos do RAG, da agenda ou das tarefas; ele apenas chama ferramentas com argumentos estruturados.

## Modos de execução
- `LLM_MODE=mock`: desenvolvimento sem consumo de tokens.
- `LLM_MODE=gemma`: validação real usando Gemma 12B via API.
