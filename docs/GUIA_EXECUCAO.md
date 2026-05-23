# Guia de execução — JARVIS Acadêmico

Este guia descreve o fluxo atual do projeto: **backend FastAPI + frontend React/Vite**. A interface antiga foi removida do fluxo de execução.

---

## Pré-requisitos

- Python 3.12 ou superior.
- Node.js 20 ou superior.
- npm.
- git.
- Internet para instalar dependências e acessar a API Gemma.

---

## 1. Clonar o projeto

```bash
git clone https://github.com/TeoZ08/jarvis-academico.git
cd jarvis-academico
```

---

## 2. Criar ambiente virtual Python

### Linux/Zorin/Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 3. Instalar dependências Python

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements_cpu.txt
```

Se estiver em ambiente com GPU ou quiser usar o arquivo principal:

```bash
python -m pip install -r requirements.txt
```

---

## 4. Configurar `.env`

```bash
cp .env.example .env
```

Editar o arquivo `.env` e preencher a chave:

```env
LLM_MODE=gemma
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_MODEL=google/gemma-3-12b-it
GEMMA_API_KEY=COLE_A_CHAVE_AQUI
GEMMA_TIMEOUT_SECONDS=180
GEMMA_MAX_TOKENS=512
RAG_MODE=hibrido
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
PYTHONUNBUFFERED=1
```

Nunca enviar `.env` para o GitHub.

---

## 5. Rodar backend FastAPI

```bash
python -m uvicorn web_api.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Endpoints úteis:

```text
http://127.0.0.1:8000/api/status
http://127.0.0.1:8000/api/debug/gemma-ping
```

---

## 6. Rodar frontend React

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

O frontend ficará disponível em:

```text
http://localhost:5173
```

---

## 7. Rodar build integrado

Para simular o deploy Docker localmente:

```bash
cd frontend
npm install
npm run build
cd ..
python -m uvicorn web_api.main:app --reload
```

Depois abrir:

```text
http://127.0.0.1:8000
```

---

## 8. Testes recomendados

```bash
python -m compileall -q src web_api scripts app.py main.py
python -m pytest
```

Também é possível gerar evidências técnicas:

```bash
python scripts/generate_evidences.py
```

---

## 9. Perguntas para validação manual

Testar na interface:

```text
O que é RAG?
Qual a diferença entre BM25 e embeddings?
O que é heap?
Inicie uma revisão ativa sobre RAG.
Registre que tenho dificuldade em BM25.
Monte um plano de estudos para a prova de IA.
```
