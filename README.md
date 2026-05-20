---
title: JARVIS Acadêmico
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# JARVIS Acadêmico

Assistente acadêmico com **RAG**, **integração com LLM Gemma 12B** e **tool calling**, desenvolvido para apoiar estudantes na organização dos estudos, consulta a materiais, geração de exercícios e planejamento de rotina acadêmica.

O projeto foi construído como uma aplicação web completa, com frontend em React, backend em FastAPI, deploy via Docker e controle de configuração por variáveis de ambiente.

---

## 1. Objetivo do projeto

O JARVIS Acadêmico funciona como um copiloto de estudos. Ele consegue:

- responder dúvidas com base em materiais cadastrados;
- recuperar fontes e chunks relevantes usando RAG;
- chamar ferramentas internas para tarefas, agenda, planejamento e geração de exercícios;
- registrar logs técnicos de tool calling;
- tratar erros e ausência de evidência com fallback acadêmico transparente;
- importar novos documentos para a base de conhecimento.

---

## 2. Requisitos atendidos

| Requisito do trabalho | Implementação no projeto |
|---|---|
| RAG | Recuperação em base local com documentos, chunks, scores e fontes exibidas na interface. |
| Integração com LLM | Uso da API compatível com OpenAI fornecida para o modelo `google/gemma-3-12b-it`. |
| Tool calling | Ferramentas internas chamadas dinamicamente e registradas em logs. |
| Avaliação e erros | Fallback acadêmico, erros controlados, endpoint de diagnóstico e painel de evidências. |
| Aprendizado | Explicações didáticas, geração de exercícios, plano de estudos e apoio ao aluno. |
| Engenharia | React, FastAPI, Docker, testes, Git, deploy online e documentação técnica. |

---

## 3. Arquitetura

```text
Usuário
  │
  ▼
Frontend React/Vite
  │
  ▼
Backend FastAPI
  ├── Agente acadêmico
  ├── Cliente LLM Gemma
  ├── Ferramentas internas
  ├── RAG / Retrieval
  ├── Storage de tarefas e agenda
  └── Logs técnicos
```

### Principais módulos

| Caminho | Função |
|---|---|
| `frontend/src/App.jsx` | Interface principal em React. |
| `frontend/src/styles.css` | Estilo visual da aplicação. |
| `web_api/main.py` | API HTTP em FastAPI. |
| `src/agent.py` | Coordenação entre usuário, LLM e ferramentas. |
| `src/llm_client.py` | Cliente da LLM Gemma/mock e diagnóstico. |
| `src/rag.py` | Indexação, recuperação e fallback RAG. |
| `src/tools.py` | Ferramentas chamadas pelo agente. |
| `src/storage.py` | Persistência local de tarefas e agenda. |
| `src/logger.py` | Registro de chamadas de ferramentas. |
| `data/` | Documentos base da disciplina. |
| `data/uploads/` | Documentos enviados pelo usuário. |
| `docs/` | Documentação técnica e análise de erros. |

---

## 4. Funcionalidades principais

### Chat acadêmico

O usuário conversa com o JARVIS e recebe respostas em Markdown, com formatação adequada para listas, títulos, código e explicações.

### RAG

O sistema recupera documentos relevantes da base de conhecimento e apresenta:

- arquivos utilizados;
- chunks recuperados;
- score de relevância;
- método de recuperação;
- diagnóstico quando não há evidência suficiente.

### Fallback acadêmico com governança

Quando a busca não encontra evidência suficiente nos materiais, o JARVIS informa explicitamente:

> Não encontrei esse tema nos materiais cadastrados. Vou responder com meu conhecimento geral da base de dados do modelo.

Isso evita confundir resposta baseada em fonte local com resposta de conhecimento geral da LLM.

### Upload de materiais

O usuário pode anexar arquivos pelo painel **Materiais** ou pelo clipe do chat. Formatos suportados:

- `.pdf`
- `.md`
- `.txt`
- `.py`

Após o upload, a base RAG é reindexada.

### Tarefas e agenda

O sistema possui ferramentas para listar, adicionar e concluir tarefas, além de consultar agenda acadêmica.

### Painel de evidências técnicas

A aba **Evidências** mostra dados úteis para avaliação:

- ferramenta chamada;
- entrada principal;
- método usado;
- top-k;
- melhor score;
- fontes recuperadas;
- fallback tratado;
- JSON bruto para auditoria.

---

## 5. Como rodar localmente

### 5.1. Clonar o repositório

```bash
git clone https://github.com/TeoZ08/jarvis-academico.git
cd jarvis-academico
```

### 5.2. Criar ambiente Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_cpu.txt
```

### 5.3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
LLM_MODE=gemma
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_MODEL=google/gemma-3-12b-it
GEMMA_API_KEY=SUA_CHAVE_AQUI
GEMMA_TIMEOUT_SECONDS=180
GEMMA_MAX_TOKENS=512
RAG_MODE=hibrido
PYTHONUNBUFFERED=1
```

Para modo de teste sem consumir API:

```env
LLM_MODE=mock
```

### 5.4. Rodar backend

```bash
python -m uvicorn web_api.main:app --reload
```

Backend local:

```text
http://127.0.0.1:8000
```

### 5.5. Rodar frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend local:

```text
http://localhost:5173
```

---

## 6. Como testar

### Testes automatizados

```bash
python -m compileall -q src web_api app.py main.py
python -m pytest
```

### Diagnóstico da Gemma

```text
/api/debug/gemma-ping
```

Resposta esperada:

```json
{
  "ok": true,
  "modo": "gemma",
  "resposta": "OK"
}
```

### Diagnóstico de configuração

```text
/api/debug/config
```

Esse endpoint informa modo da LLM, presença de chave e parâmetros sem expor segredos.

### Perguntas recomendadas para validação

```text
O que é RAG?
```

Deve acionar RAG e apresentar fontes.

```text
O que é heap?
```

Deve acionar busca, detectar ausência de evidência suficiente e usar fallback acadêmico.

```text
Monte um plano de estudos para a prova de IA.
```

Deve usar ferramentas de planejamento, tarefas e agenda.

```text
Gere 3 exercícios sobre embeddings.
```

Deve gerar exercício didático ligado ao conteúdo acadêmico.

---

## 7. Deploy

### Hugging Face Spaces

O projeto está preparado para Docker Spaces. O cabeçalho YAML deste README informa:

```yaml
sdk: docker
app_port: 7860
```

Variáveis recomendadas no Space:

```env
LLM_MODE=gemma
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_MODEL=google/gemma-3-12b-it
GEMMA_TIMEOUT_SECONDS=180
GEMMA_MAX_TOKENS=512
RAG_MODE=hibrido
PYTHONUNBUFFERED=1
```

Secret obrigatório:

```env
GEMMA_API_KEY=SUA_CHAVE_AQUI
```

A chave deve ficar em **Secrets**, não em variável pública.

### Render

O projeto também possui arquivos de deploy para Render:

- `Dockerfile`
- `render.yaml`
- `Procfile`
- `runtime.txt`

Em ambientes gratuitos com pouca memória, recomenda-se usar:

```env
RAG_MODE=lexical
```

---

## 8. Ferramentas e bibliotecas utilizadas

### Desenvolvimento

- Python
- FastAPI
- Uvicorn
- React
- Vite
- Docker
- Git/GitHub
- Hugging Face Spaces
- Render

### IA/RAG

- OpenAI Python SDK compatível com API LIA/UFMS
- Gemma 12B (`google/gemma-3-12b-it`)
- Sentence Transformers
- FAISS CPU
- BM25 / `rank_bm25`
- scikit-learn
- pandas
- numpy

### Interface

- React Markdown
- remark-gfm
- lucide-react

---

## 9. Decisões técnicas importantes

### Separação frontend/backend

O frontend React é independente do backend FastAPI. Isso melhora a manutenção e permite deploy moderno.

### Variáveis de ambiente

Chaves e configurações ficam fora do código. A API key da Gemma nunca deve ser commitada.

### Fallback transparente

O sistema diferencia respostas baseadas nos materiais locais de respostas feitas com conhecimento geral da LLM.

### Logs auditáveis

Cada ferramenta registra entrada e saída. A interface exibe uma versão amigável e mantém o JSON bruto disponível.

### Diagnóstico de LLM

Foram criados endpoints de debug para isolar problemas de token, URL, timeout e conectividade.

---

## 10. Limitações conhecidas

- O desempenho do RAG híbrido depende da memória disponível no servidor.
- Em deploys gratuitos, pode haver cold start e lentidão inicial.
- A qualidade das respostas depende da qualidade dos documentos cadastrados.
- Quando um tema não está na base local, o sistema usa fallback acadêmico com aviso.
- A API institucional pode ter limite de uso e deve ser preservada.

---

## 11. Segurança

Não versionar:

- `.env`
- tokens de Hugging Face;
- `GEMMA_API_KEY`;
- arquivos privados com credenciais.

O `.gitignore` deve bloquear `.env`, cache, ambientes virtuais e arquivos temporários.

---

## 12. Status do projeto

| Item | Status |
|---|---|
| Frontend React | Implementado |
| Backend FastAPI | Implementado |
| RAG | Implementado |
| Tool calling | Implementado |
| Gemma 12B | Implementado |
| Upload de documentos | Implementado |
| Fallback acadêmico | Implementado |
| Logs/evidências | Implementado |
| Deploy Docker | Implementado |
| Testes | Implementado |
