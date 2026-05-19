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


## Upload de documentos

A interface Streamlit usa `st.file_uploader` para receber arquivos `.pdf`, `.md`, `.txt` e `.py`. Os arquivos são salvos em `data/uploads/`. Após salvar, o cache do RAG e do agente é limpo para forçar nova indexação dos materiais.

## Fallback acadêmico com governança

Foi adicionada uma camada de transparência para perguntas acadêmicas fora da base local. O objetivo é evitar dois problemas comuns em sistemas RAG:

1. o assistente parecer incapaz quando o tema não está nos documentos;
2. o assistente responder com conhecimento geral fingindo que usou os materiais.

O fluxo é:

```text
Pergunta acadêmica → buscar_material_rag → diagnóstico de relevância
                                      ↓
                    evidência suficiente? sim → resposta baseada no RAG
                                      ↓ não
                    RESULTADO_VAZIO → resposta geral com aviso de fonte
```

O diagnóstico de relevância considera a sobreposição de termos relevantes da pergunta com o contexto recuperado e a similaridade densa bruta. Isso é necessário porque o score híbrido é normalizado e pode parecer alto mesmo quando o tema está fora da base.

## Camada web FastAPI

A versão premium adiciona uma camada web independente do Streamlit:

```text
frontend/index.html
frontend/assets/styles.css
frontend/assets/app.js
        ↓ fetch()
web_api/main.py
        ↓
src/agent.py + src/tools.py + src/rag.py
```

Essa separação permite publicar o projeto online mantendo a lógica principal isolada em módulos profundos. O frontend não acessa diretamente a chave da Gemma; todas as chamadas sensíveis passam pelo backend FastAPI.

## Por que não usar apenas GitHub Pages?

GitHub Pages é adequado para frontend estático. Porém, este projeto precisa executar Python, carregar embeddings, manter storage local, processar uploads, chamar ferramentas e conversar com a API Gemma. Por isso, para uma versão funcional online, é necessário um backend Python hospedado em serviço compatível com ASGI/FastAPI.
