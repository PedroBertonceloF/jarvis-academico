# Guia de execução em outro computador

Este guia descreve como executar o JARVIS Acadêmico localmente em outro computador.

## Pré-requisitos

- Python 3.10 ou superior.
- Node.js 18 ou superior.
- npm.
- git.
- Internet para instalar dependências.
- Chave da API Gemma, quando for testar o modo real com LLM.

## 1. Clonar o projeto

```bash
git clone https://github.com/TeoZ08/jarvis-academico.git
cd jarvis-academico
```

## 2. Criar e ativar ambiente Python

### Linux/Zorin/Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

## 3. Instalar dependências do backend

Instalação padrão:

```bash
python -m pip install -r requirements.txt
```

Em ambiente com menos memória, pode ser usado o arquivo de dependências para CPU:

```bash
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements_cpu.txt
```

## 4. Configurar `.env`

Crie o arquivo local a partir do exemplo:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
copy .env.example .env
```

Configuração recomendada para usar Gemma:

```env
LLM_MODE=gemma
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_MODEL=google/gemma-3-12b-it
GEMMA_API_KEY=SUA_CHAVE_SEM_ASPAS
GEMMA_TIMEOUT_SECONDS=180
GEMMA_MAX_TOKENS=512
RAG_MODE=hibrido
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
PYTHONUNBUFFERED=1
```

Para desenvolvimento sem consumir API, é possível usar:

```env
LLM_MODE=mock
```

O arquivo `.env` nunca deve ser enviado para o GitHub.

## 5. Rodar o backend FastAPI

```bash
python -m uvicorn web_api.main:app --reload
```

Backend local:

```text
http://127.0.0.1:8000
```

Endpoints úteis:

```text
http://127.0.0.1:8000/api/status
http://127.0.0.1:8000/api/debug/config
http://127.0.0.1:8000/api/debug/gemma-ping
```

## 6. Rodar o frontend React em desenvolvimento

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend local:

```text
http://127.0.0.1:5173
```

O Vite redireciona chamadas `/api` para o backend FastAPI.

## 7. Rodar o frontend integrado ao FastAPI

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

## 8. Testes recomendados

No app, testar:

```text
O que é RAG?
```

```text
Qual a diferença entre BM25 e embeddings?
```

```text
O que é heap?
```

```text
Inicie uma revisão ativa sobre RAG.
```

```text
Registre que tenho dificuldade em BM25.
```

```text
Monte um plano de estudos para a prova de IA.
```

## 9. Testes automatizados

```bash
python -m compileall -q src web_api app.py main.py
python -m pytest
```

## 10. Observações de segurança

- Não versionar `.env`.
- Não expor `GEMMA_API_KEY` em prints, commits ou README.
- No Hugging Face, a chave deve ficar em Secrets.
- O frontend não deve acessar diretamente a chave da Gemma.
