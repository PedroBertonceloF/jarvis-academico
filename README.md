# JARVIS Acadêmico — Assistente Inteligente para Estudantes

Projeto prático da disciplina de Inteligência Artificial.

O sistema implementa RAG, tool calling com Gemma 12B, agenda acadêmica, lista de tarefas, planejamento de estudos, logs, avaliação e funcionalidades de aprendizagem.

## Funcionalidades

- Consulta a materiais de estudo com RAG.
- Importação de documentos pela interface Streamlit (`.pdf`, `.md`, `.txt` e `.py`).
- Agenda acadêmica local em JSON.
- Lista de tarefas com adicionar, listar e concluir.
- Planejamento de estudos combinando agenda, tarefas e materiais.
- Tool calling decidido pela LLM.
- Logs das ferramentas chamadas.
- Geração de exercícios e active recall.
- Script de avaliação com 10 perguntas.
- Modo `mock` para desenvolvimento sem consumir tokens.

## Arquitetura resumida

```text
Usuário → Streamlit/CLI → JarvisAgent → GemmaClient → ToolRegistry
                                      ↓
           RAG / Agenda / Tarefas / Planejamento / Exercícios
                                      ↓
                         logs/tool_calls.jsonl
```

Mais detalhes em `docs/ARQUITETURA.md`.

## Instalação recomendada — Linux/Zorin/Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements_cpu.txt
cp .env.example .env
```

Edite o `.env`.

Para desenvolvimento sem consumir tokens:

```env
LLM_MODE=mock
```

Para teste final/vídeo com Gemma:

```env
LLM_MODE=gemma
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_API_KEY=CHAVE_FORNECIDA_PELO_PROFESSOR
GEMMA_MODEL=google/gemma-3-12b-it
```

Nunca suba `.env` para o GitHub.

## Executar

Interface gráfica:

```bash
python -m streamlit run app.py
```

Terminal:

```bash
python main.py
```

## Verificações

```bash
python -m compileall -q src app.py main.py
python -m pytest
python scripts/check_dataset.py
python scripts/evaluate_system.py
```

## Dataset

A pasta `data/` contém 10 documentos acadêmicos iniciais em Markdown, cobrindo RAG, BM25, embeddings, FAISS, KNN, normalização, gradiente descendente, regressão linear, regressão logística e tool calling.

Também é possível importar novos materiais pela barra lateral da interface. Os arquivos enviados são salvos em `data/uploads/` e a base pode ser reindexada em seguida.

Documentação do dataset: `data/README_DATASET.md`.

## Tool calling

Ferramentas implementadas:

1. `consultar_agenda`
2. `listar_tarefas`
3. `adicionar_tarefa`
4. `concluir_tarefa`
5. `buscar_material_rag`
6. `gerar_exercicios`
7. `planejar_estudos`

Logs:

```text
logs/tool_calls.jsonl
```

Cada log contém timestamp, ferramenta chamada, entrada e saída.

## Documentação da entrega

Arquivos principais:

- `docs/PRD.md`
- `docs/ARQUITETURA.md`
- `docs/KANBAN.md`
- `docs/AVALIACAO_10_PERGUNTAS.md`
- `docs/ANALISE_DE_ERROS.md`
- `docs/DECISOES_TECNICAS.md`
- `docs/GUIA_EXECUCAO.md`

## Sugestão de roteiro para vídeo de até 3 minutos

1. Mostrar rapidamente a arquitetura.
2. Mostrar os documentos em `data/`.
3. Perguntar: “Explique regressão logística”.
4. Perguntar: “Liste minhas tarefas”.
5. Pedir: “Monte um plano de estudos para a prova de IA”.
6. Mostrar `logs/tool_calls.jsonl`.
7. Mostrar active recall ou geração de exercícios.
8. Explicar que o modo mock é usado para desenvolvimento e Gemma para validação final.

## IAs utilizadas

Preencher conforme o uso real do grupo. Sugestão:

- ChatGPT: apoio na estruturação, revisão e documentação.
- Gemma 12B: LLM usada em execução real do sistema.

## Fallback acadêmico com transparência

O JARVIS usa o RAG como fonte primária para dúvidas acadêmicas. Quando o usuário pergunta algo que não aparece nos materiais cadastrados, o sistema não apresenta uma resposta como se ela viesse dos documentos.

Fluxo implementado:

1. A LLM decide chamar `buscar_material_rag` para verificar os materiais locais.
2. O RAG calcula sinais de relevância, como termos encontrados no contexto e similaridade densa.
3. Se não houver evidência suficiente, a ferramenta retorna `resultado_vazio=true` e a mensagem `RESULTADO_VAZIO`.
4. O agente gera uma resposta de conhecimento geral iniciando com o aviso obrigatório:

```text
Não encontrei esse tema nos materiais cadastrados. Vou responder com meu conhecimento geral da base de dados do modelo.
```

Esse comportamento evita a “cegueira de contexto” sem enfraquecer o RAG. O usuário sabe quando a resposta veio dos materiais e quando veio do conhecimento geral da LLM.


## Interface Web Premium

Além do protótipo em Streamlit, o projeto possui uma interface web própria com FastAPI + HTML/CSS/JS.

Rodar localmente:

```bash
source .venv/bin/activate
python -m uvicorn web_api.main:app --reload
```

Acesse:

```text
http://127.0.0.1:8000
```

A interface web oferece:

- chat acadêmico com JARVIS;
- painel de fontes recuperadas pelo RAG;
- painel de ferramentas chamadas;
- upload de documentos;
- listagem e criação de tarefas;
- consulta e criação de eventos de agenda;
- visualização de logs técnicos.

O Streamlit (`app.py`) foi mantido como plano B de execução.

## Deploy online

A aplicação pode ser publicada em serviços que executam Python/FastAPI, como Render ou Railway.

O arquivo `render.yaml` contém uma configuração inicial para deploy no Render. Recomenda-se iniciar em `LLM_MODE=mock` e ativar `LLM_MODE=gemma` apenas para homologação ou gravação, evitando consumo excessivo da API do LIA.

Comando de start esperado:

```bash
uvicorn web_api.main:app --host 0.0.0.0 --port $PORT
```

Importante: nunca coloque `GEMMA_API_KEY` no frontend nem no GitHub. Configure a chave apenas nas variáveis de ambiente da plataforma de deploy.
