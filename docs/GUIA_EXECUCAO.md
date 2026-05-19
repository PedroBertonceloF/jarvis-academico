# Guia de execução em outro computador

## Pré-requisitos
- Python 3.10 ou superior.
- pip.
- git.
- Internet para instalar dependências.

## Linux/Zorin/Ubuntu

```bash
git clone LINK_DO_REPOSITORIO
cd jarvis_academico
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements_cpu.txt
cp .env.example .env
python -m streamlit run app.py
```

## Windows PowerShell

```powershell
git clone LINK_DO_REPOSITORIO
cd jarvis_academico
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
copy .env.example .env
python -m streamlit run app.py
```

## Configuração do `.env`

Para desenvolver sem gastar tokens:

```env
LLM_MODE=mock
```

Para testar com Gemma:

```env
LLM_MODE=gemma
GEMMA_API_KEY=CHAVE_FORNECIDA_PELO_PROFESSOR
```

Nunca envie `.env` para o GitHub.
