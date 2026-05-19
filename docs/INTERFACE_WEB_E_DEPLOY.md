# Interface Web e Deploy

## Objetivo

A nova interface transforma o JARVIS Acadêmico de um protótipo em Streamlit em uma aplicação web com aparência de produto. O Streamlit continua como plano B, mas a experiência principal passa a ser:

```text
frontend/  -> HTML, CSS e JavaScript
web_api/   -> FastAPI
src/       -> RAG, Agent, Tool Calling, agenda, tarefas e storage
```

## Decisão arquitetural

A interface web não acessa diretamente arquivos Python internos. Ela se comunica com a API por endpoints HTTP.

Principais endpoints:

- `GET /` — abre a interface web.
- `GET /api/status` — mostra modo LLM, documentos e chunks.
- `POST /api/chat` — envia mensagem ao JARVIS.
- `POST /api/upload` — importa documentos para `data/uploads` e reindexa a base.
- `GET /api/tasks` — lista tarefas.
- `POST /api/tasks` — adiciona tarefa.
- `PATCH /api/tasks/{id}/complete` — conclui tarefa.
- `GET /api/agenda` — lista agenda.
- `GET /api/logs` — exibe logs de ferramentas.

## Identidade visual

A direção visual segue a ideia:

```text
Notion clean + JARVIS command center + inspiração discreta em Vision
```

Características:

- fundo escuro sofisticado;
- cards limpos e arredondados;
- acentos em ciano, dourado e roxo;
- destaque para fontes recuperadas e ferramentas chamadas;
- visual técnico sem depender de imagens ou marcas protegidas.

## Deploy recomendado

Para manter o projeto simples e funcional online, a recomendação é hospedar a aplicação inteira em um backend FastAPI que também serve o frontend estático.

### Render

Configuração sugerida:

- Build Command:

```bash
python -m pip install --upgrade pip setuptools wheel && python -m pip install torch --index-url https://download.pytorch.org/whl/cpu && python -m pip install -r requirements_cpu.txt
```

- Start Command:

```bash
uvicorn web_api.main:app --host 0.0.0.0 --port $PORT
```

- Variáveis de ambiente:

```env
LLM_MODE=mock
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_API_KEY=COLE_A_CHAVE_NO_PAINEL_DO_RENDER
GEMMA_MODEL=google/gemma-3-12b-it
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Para demonstração pública, recomenda-se manter `LLM_MODE=mock`. Para vídeo ou homologação, usar `LLM_MODE=gemma` com cuidado para controlar consumo de tokens.

## Execução local da interface web

```bash
source .venv/bin/activate
python -m uvicorn web_api.main:app --reload
```

Abrir:

```text
http://127.0.0.1:8000
```

## Observações importantes

- A chave da Gemma nunca deve ficar no frontend.
- A chave da Gemma nunca deve ser commitada no GitHub.
- `data/uploads/*` deve ser ignorado no Git, mantendo apenas `data/uploads/.gitkeep`.
- O modelo de embeddings pode deixar o deploy mais pesado; por isso, o Render/Railway são mais adequados que GitHub Pages para execução real.
