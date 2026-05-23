# Arquitetura do JARVIS Acadêmico

## Visão geral

O JARVIS Acadêmico é uma aplicação web com arquitetura cliente-servidor:

```text
Frontend React
  │ HTTP/JSON
  ▼
Backend FastAPI
  ├── Agente acadêmico
  ├── Cliente LLM Gemma
  ├── Tool calling
  ├── RAG
  ├── Storage
  └── Logs
```

O objetivo arquitetural é separar interface, lógica de agente, recuperação de informação e persistência.

---

## Frontend

Local:

```text
frontend/
```

Tecnologias:

- React;
- Vite;
- React Markdown;
- lucide-react;
- CSS customizado.

Responsabilidades:

- chat acadêmico;
- upload de documentos;
- visualização de fontes;
- tarefas;
- agenda;
- painel de evidências técnicas;
- exibição de erros controlados.

---

## Backend

Local:

```text
web_api/main.py
```

Tecnologia:

- FastAPI;
- Uvicorn;
- Docker.

Responsabilidades:

- servir API REST;
- servir frontend compilado;
- receber upload de arquivos;
- expor status do sistema;
- expor logs;
- diagnosticar Gemma;
- integrar agente, RAG, ferramentas e storage.

---

## Agente

Local:

```text
src/agent.py
```

Responsabilidades:

- receber a mensagem do usuário;
- decidir ferramentas;
- executar tool calling;
- montar resposta final;
- tratar fallback acadêmico;
- retornar resposta, fontes e logs para a interface.

---

## LLM

Local:

```text
src/llm_client.py
```

Modos:

| Modo | Função |
|---|---|
| `gemma` | Usa a API Gemma 12B fornecida. |
| `mock` | Modo auxiliar local para desenvolvimento sem consumo de API. Não é o modo oficial da entrega. |

Variáveis principais:

```env
LLM_MODE=gemma
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_MODEL=google/gemma-3-12b-it
GEMMA_API_KEY=...
GEMMA_TIMEOUT_SECONDS=180
GEMMA_MAX_TOKENS=512
```

---

## RAG

Local:

```text
src/rag.py
```

Base:

```text
data/
data/uploads/
```

Estratégias:

| Modo | Descrição |
|---|---|
| `lexical` | Recuperação por BM25/palavras-chave. |
| `hibrido` | Combinação de busca lexical e embeddings. |

Fluxo:

```text
Documento → chunking → indexação → recuperação → contexto → resposta
```

---

## Tool calling

Local:

```text
src/tools.py
```

Ferramentas principais:

- `buscar_material_rag`;
- `planejar_estudos`;
- `gerar_exercicios`;
- `listar_tarefas`;
- `adicionar_tarefa`;
- `concluir_tarefa`;
- `consultar_agenda`.

Cada chamada é registrada com:

- timestamp;
- nome da ferramenta;
- entrada;
- saída;
- documentos recuperados, quando aplicável.

---

## Logs e evidências

Local:

```text
src/logger.py
logs/
```

A interface transforma logs técnicos em evidências legíveis:

- ferramenta executada;
- entrada principal;
- método de recuperação;
- top-k;
- melhor score;
- documentos recuperados;
- fallback acadêmico;
- JSON bruto.

---

## Deploy

### Hugging Face Spaces

Recomendado para rodar o projeto completo com Docker.

Porta padrão:

```text
7860
```

## Segurança

Segredos não ficam versionados.

A `GEMMA_API_KEY` deve ser configurada em:

- `.env` local; ou
- Secrets do Hugging Face.

Nunca deve ser colocada no código ou no README.
