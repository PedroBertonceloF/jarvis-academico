# JARVIS Acadêmico — Assistente Inteligente para Estudantes

Projeto prático da disciplina de Inteligência Artificial.

O sistema implementa RAG, tool calling com Gemma 12B, agenda acadêmica, lista de tarefas, planejamento de estudos, logs, avaliação e funcionalidades de aprendizagem.

## Funcionalidades

- Consulta a materiais de estudo com RAG.
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
