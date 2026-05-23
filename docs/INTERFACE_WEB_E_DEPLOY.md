# Interface Web e Deploy

## Objetivo

A interface principal do JARVIS Acadêmico é uma aplicação web em React + Vite, integrada a um backend FastAPI. A proposta é transformar o projeto em um assistente acadêmico com aparência de produto, mantendo uma arquitetura simples para demonstração e avaliação.

Estrutura principal:

```text
frontend/  -> React, Vite e interface do usuário
web_api/   -> FastAPI, endpoints e servidor do frontend compilado
src/       -> RAG, agente, tool calling, agenda, tarefas, aprendizado e storage
```

## Decisão arquitetural

A interface web não acessa diretamente os módulos Python internos. Ela se comunica com a API por endpoints HTTP.

Principais endpoints:

- `GET /` — abre a interface web.
- `GET /api/status` — mostra modo LLM, documentos e chunks.
- `GET /api/debug/config` — mostra configuração técnica sem expor segredos.
- `GET /api/debug/gemma-ping` — testa a conexão com a Gemma.
- `POST /api/chat` — envia mensagem ao JARVIS.
- `POST /api/upload` — importa documentos e reindexa a base.
- `GET /api/tasks` — lista tarefas.
- `POST /api/tasks` — adiciona tarefa.
- `PATCH /api/tasks/{id}/complete` — conclui tarefa.
- `GET /api/agenda` — lista agenda.
- `GET /api/logs` — exibe logs de ferramentas.

## Identidade visual

A direção visual segue a ideia:

```text
Notion clean + JARVIS command center + painel técnico de evidências
```

Características:

- fundo escuro sofisticado;
- cards limpos e arredondados;
- acentos visuais tecnológicos;
- destaque para fontes recuperadas pelo RAG;
- painel de ferramentas chamadas;
- aba de evidências técnicas para apoiar a correção do professor.

## Deploy oficial

O deploy oficial do projeto é o Hugging Face Spaces com Docker.

Link do Space:

```text
https://huggingface.co/spaces/TeoZ08/jarvis-academico
```

Link direto provável do app:

```text
https://teoz08-jarvis-academico.hf.space
```

O `README.md` deve manter no topo absoluto o cabeçalho YAML do Hugging Face:

```yaml
---
title: JARVIS Acadêmico
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---
```

Não pode haver linha em branco antes desse bloco.

## Variáveis de ambiente no Hugging Face

Em Variables:

```env
LLM_MODE=gemma
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_MODEL=google/gemma-3-12b-it
GEMMA_TIMEOUT_SECONDS=180
GEMMA_MAX_TOKENS=512
RAG_MODE=hibrido
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
PYTHONUNBUFFERED=1
```

Em Secrets:

```env
GEMMA_API_KEY=SUA_CHAVE_SEM_ASPAS
```

A chave não deve ter aspas e não deve ser colocada em Variables.

## Deploy alternativo

O Render foi testado como alternativa, mas apresentou limitação de memória no plano gratuito. Por isso, ele não é o deploy principal da entrega.

Caso seja usado, pode ser necessário configurar:

```env
RAG_MODE=lexical
```

para reduzir consumo de memória.

## Execução local da interface web

Backend:

```bash
source .venv/bin/activate
python -m uvicorn web_api.main:app --reload
```

Frontend em desenvolvimento:

```bash
cd frontend
npm install
npm run dev
```

Abrir:

```text
http://127.0.0.1:5173
```

Frontend integrado ao backend:

```bash
cd frontend
npm install
npm run build
cd ..
python -m uvicorn web_api.main:app --reload
```

Abrir:

```text
http://127.0.0.1:8000
```

## Validação recomendada no deploy

Testar:

```text
https://teoz08-jarvis-academico.hf.space/api/status
https://teoz08-jarvis-academico.hf.space/api/debug/gemma-ping
https://teoz08-jarvis-academico.hf.space
```

Perguntas recomendadas no app:

```text
O que é RAG?
O que é heap?
Inicie uma revisão ativa sobre RAG.
Registre que tenho dificuldade em BM25.
Monte um plano de estudos para a prova de IA.
```

## Observações importantes

- A chave da Gemma nunca deve ficar no frontend.
- A chave da Gemma nunca deve ser commitada no GitHub.
- `data/uploads/*` deve ser ignorado no Git, mantendo apenas `.gitkeep` quando necessário.
- O Hugging Face Spaces com Docker é o ambiente oficial da entrega.
