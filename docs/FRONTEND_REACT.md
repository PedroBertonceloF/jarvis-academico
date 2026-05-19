# Frontend React — JARVIS Acadêmico

Esta versão substitui a interface web HTML/CSS/JS simples por uma interface em **React + Vite**, mantendo o backend FastAPI e toda a lógica existente em `src/`.

## Objetivo da mudança

A interface React foi criada para transformar o JARVIS em um produto mais polido:

- chat com renderização Markdown;
- respostas com títulos, listas, negrito, blocos de código e hierarquia visual;
- painel lateral de fontes recuperadas pelo RAG;
- painel de ferramentas chamadas pela LLM;
- upload de documentos;
- tarefas, agenda e logs em telas próprias;
- identidade visual inspirada em Notion + JARVIS/Vision, sem copiar marcas protegidas.

## Como rodar em desenvolvimento

Terminal 1 — backend:

```bash
source .venv/bin/activate
python -m uvicorn web_api.main:app --reload
```

Terminal 2 — frontend:

```bash
cd frontend
npm install
npm run dev
```

Abra:

```text
http://127.0.0.1:5173
```

O Vite redireciona chamadas `/api` para o FastAPI em `http://127.0.0.1:8000`.

## Como rodar integrado pelo FastAPI

Gere o build do React:

```bash
cd frontend
npm install
npm run build
cd ..
```

Depois rode:

```bash
python -m uvicorn web_api.main:app --reload
```

Abra:

```text
http://127.0.0.1:8000
```

## Testes recomendados

1. `O que é RAG?`  
   Deve usar RAG e exibir fontes.

2. `O que é heap?`  
   Deve acionar fallback acadêmico com aviso de fonte.

3. `Monte um plano de estudos para a prova de IA.`  
   Deve usar tool calling, tarefas, agenda e materiais relevantes.

4. Upload de PDF/TXT/MD/PY em **Materiais**.  
   Deve salvar em `data/uploads/`, reindexar e atualizar a base.

## Observações de segurança

- A chave da Gemma nunca deve ir para o frontend.
- O frontend chama apenas o backend.
- A variável `GEMMA_API_KEY` deve ficar no `.env` local ou no painel de variáveis do serviço de deploy.
- `frontend/.env` e `frontend/.env.local` estão ignorados pelo Git.

## Deploy

Para deploy real online, prefira hospedar o backend FastAPI e o frontend React no mesmo serviço via build do Vite. O `Dockerfile` do projeto já contempla esse fluxo.
