---
title: JARVIS Acadêmico
emoji: 🧠
colorFrom: indigo
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---


# JARVIS Acadêmico — Assistente com RAG, Gemma 12B e Tool Calling

Projeto prático da disciplina de **Inteligência Artificial — FACOM/UFMS**.

O **JARVIS Acadêmico** é um assistente pessoal acadêmico desenvolvido para apoiar estudantes na organização dos estudos e na compreensão de conteúdos da disciplina. O sistema combina **RAG**, **integração com LLM Gemma 12B**, **tool calling**, upload de documentos, planejamento de estudos, geração de exercícios e painel técnico de evidências.

## Link do projeto online

O projeto está disponível no Hugging Face Spaces:

https://huggingface.co/spaces/TeoZ08/jarvis-academico


---

## 1. Objetivo do projeto

O objetivo do JARVIS Acadêmico é atuar como um copiloto de estudos para alunos de Computação, com foco em:

- responder dúvidas sobre conteúdos acadêmicos;
- consultar materiais cadastrados por meio de RAG;
- gerar planos de estudo;
- sugerir exercícios;
- gerar sessões de revisão ativa com perguntas baseadas no RAG;
- avaliar respostas do aluno e registrar dificuldades;
- registrar evidências técnicas de tool calling;
- demonstrar integração real com uma LLM obrigatória;
- apoiar o aprendizado de forma transparente e rastreável.

O projeto foi desenvolvido com foco nos critérios avaliativos do trabalho:

| Critério | Peso |
|---|---:|
| Funcionalidade | 20% |
| RAG | 20% |
| Tool calling | 15% |
| Avaliação + erros | 20% |
| Aprendizado | 15% |
| Engenharia | 10% |

---

## 2. Funcionalidades principais

### Chat acadêmico

O usuário pode conversar com o JARVIS sobre temas da disciplina de Inteligência Artificial e sobre conceitos gerais de Computação.

Exemplos de perguntas:

```text
O que é RAG?
Explique regressão logística.
O que é heap?
Monte um plano de estudos para a prova de IA.
Gere 3 exercícios sobre embeddings.
```

### RAG com fontes

O sistema recupera trechos dos materiais cadastrados e usa esses trechos como contexto para a resposta da LLM.

A interface exibe:

- fontes recuperadas;
- score de similaridade;
- chunks utilizados;
- método de recuperação;
- evidência de uso do RAG.

### Upload de documentos

O usuário pode anexar documentos pela interface.

Formatos previstos:

- `.md`;
- `.txt`;
- `.pdf`.

Os arquivos enviados são processados, divididos em chunks e incorporados ao mecanismo de busca do RAG.

### Tool calling

O sistema possui ferramentas internas que podem ser chamadas pelo agente, como:

- busca em materiais via RAG;
- planejamento de estudos;
- listagem, criação e conclusão de tarefas;
- consulta e criação de eventos de agenda;
- geração de exercícios;
- sessões de revisão ativa;
- avaliação de respostas do aluno;
- registro de dificuldades para personalização de estudos;
- diagnóstico da Gemma.

Cada chamada de ferramenta é registrada no painel de evidências técnicas.

### Fallback acadêmico

Quando o tema perguntado não aparece nos materiais cadastrados, o sistema não inventa fonte.

Ele informa que não encontrou o tema no dataset e responde com conhecimento geral do modelo, sinalizando a origem da resposta.

Exemplo:

```text
Não encontrei esse tema nos materiais cadastrados.
Vou responder com meu conhecimento geral da base de dados do modelo.
```

Esse comportamento melhora a transparência e reduz o risco de alucinação.

### Revisão ativa e dificuldades

O projeto incorporou uma camada de aprendizado ativo inspirada na versão complementar desenvolvida pelo grupo. Essa camada permite:

- gerar uma pergunta de revisão com base nos materiais recuperados pelo RAG;
- salvar um `review_id` para a sessão de revisão;
- avaliar a resposta do aluno usando Gemma;
- classificar a resposta como `CORRECT`, `PARTIAL` ou `INCORRECT`;
- registrar automaticamente tópicos de dificuldade quando a resposta for parcial ou incorreta;
- usar dificuldades recentes como contexto adicional no plano de estudos.

Essa melhoria reforça os critérios de **Aprendizado**, **Tool calling**, **Funcionalidade** e **Avaliação + erros**.

---

## 3. Origem dos dados do dataset

O dataset inicial do JARVIS Acadêmico é composto por documentos locais em formato Markdown, armazenados na pasta `data/`.

Esses documentos foram criados manualmente para representar conteúdos centrais da disciplina de Inteligência Artificial, incluindo:

- RAG;
- BM25;
- embeddings;
- FAISS;
- KNN;
- normalização;
- gradiente descendente;
- regressão linear;
- regressão logística;
- tool calling.

Além da base inicial, o sistema permite que o usuário importe novos materiais acadêmicos pela interface web. Esses arquivos são salvos localmente, processados em chunks e incorporados ao mecanismo de recuperação.

Portanto, os dados utilizados pelo sistema têm origem **local, controlada e expansível**.

O JARVIS não coleta dados automaticamente da internet. A base de conhecimento é formada por materiais previamente cadastrados no projeto e por documentos adicionados pelo próprio usuário.

---

## 4. Arquitetura do sistema

A arquitetura geral é composta por:

```text
Frontend React
      ↓
Backend FastAPI
      ↓
Agente acadêmico
      ↓
Tool calling
      ↓
RAG + Agenda + Tarefas + Exercícios
      ↓
Gemma 12B via API
```

### Componentes principais

| Componente | Função |
|---|---|
| `frontend/` | Interface web em React |
| `web_api/` | API FastAPI usada pelo frontend |
| `src/agent.py` | Orquestra o comportamento do assistente |
| `src/llm_client.py` | Integração com a API Gemma |
| `src/rag.py` | Indexação e recuperação dos documentos |
| `src/tools.py` | Ferramentas chamadas pelo agente |
| `data/` | Dataset acadêmico inicial |
| `docs/` | Documentação técnica |
| `tests/` | Testes automatizados |

---

## 5. RAG

O projeto implementa RAG para recuperar trechos relevantes antes de gerar respostas.

O pipeline é:

```text
Documento
   ↓
Chunking
   ↓
Indexação
   ↓
Busca lexical / híbrida
   ↓
Recuperação dos trechos relevantes
   ↓
Prompt com contexto
   ↓
Resposta gerada pela LLM
```

### Estratégias de recuperação

O sistema foi preparado para trabalhar com:

- busca lexical;
- BM25;
- embeddings;
- FAISS;
- recuperação híbrida.

No ambiente online, a configuração pode ser ajustada por variável de ambiente:

```env
RAG_MODE=hibrido
```

ou, em ambientes com pouca memória:

```env
RAG_MODE=lexical
```

---

## 6. Integração com LLM

A LLM obrigatória utilizada é:

```text
Gemma 12B
```

Modelo configurado:

```env
GEMMA_MODEL=google/gemma-3-12b-it
```

URL da API:

```env
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
```

A chave de API deve ser configurada em variável de ambiente ou secret:

```env
GEMMA_API_KEY=sua_chave_aqui
```


---

## 7. Tool calling

O sistema implementa tool calling para permitir que a LLM acione ferramentas internas.

Exemplos de ferramentas:

| Ferramenta | Função |
|---|---|
| `buscar_material_rag` | Busca trechos relevantes nos materiais |
| `planejar_estudos` | Gera plano de estudos |
| `listar_tarefas` | Consulta tarefas acadêmicas |
| `consultar_agenda` | Consulta compromissos simulados |
| `adicionar_evento` | Cria eventos acadêmicos na agenda |
| `gerar_exercicios` | Cria exercícios com base nos conteúdos |
| `iniciar_revisao` | Gera uma pergunta de active recall baseada no RAG |
| `avaliar_resposta_revisao` | Avalia a resposta do aluno e registra dificuldade |
| `registrar_dificuldade` | Salva dificuldades para personalizar planos |

A aba **Evidências Técnicas** mostra:

- ferramenta chamada;
- entrada da ferramenta;
- saída resumida;
- fontes recuperadas;
- scores;
- fallback;
- JSON técnico bruto.

Essa tela foi criada para facilitar a correção do requisito de tool calling.

---

## 8. Avaliação, erros e governança

O projeto possui tratamento controlado para diferentes situações:

### Tema fora do dataset

Quando a busca não encontra evidência suficiente, o sistema usa fallback acadêmico com aviso explícito.

### Token inválido

Quando a chave da Gemma está incorreta, o sistema retorna erro controlado.

### Timeout

O sistema possui variáveis para controlar tempo máximo de espera:

```env
GEMMA_TIMEOUT_SECONDS=180
```

### Limite de tokens

A quantidade máxima de tokens da resposta pode ser ajustada:

```env
GEMMA_MAX_TOKENS=512
```

### Diagnóstico da Gemma

Foi criado um endpoint de diagnóstico:

```text
/api/debug/gemma-ping
```

Esse endpoint testa a comunicação direta com a Gemma sem passar pelo fluxo completo do agente.

Exemplo de retorno esperado:

```json
{
  "ok": true,
  "modo": "gemma",
  "resposta": "OK",
  "api_key_presente": true
}
```

---

## 9. Como executar localmente

### Pré-requisitos

- Python 3.12+
- Node.js
- npm
- Git

### Clonar o projeto

```bash
git clone https://github.com/TeoZ08/jarvis-academico.git
cd jarvis-academico
```

### Criar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalar dependências Python

```bash
pip install --upgrade pip
pip install -r requirements_cpu.txt
```

Se necessário:

```bash
pip install -r requirements.txt
```

### Criar arquivo `.env`

Na raiz do projeto:

```bash
nano .env
```

Exemplo:

```env
LLM_MODE=gemma
GEMMA_BASE_URL=https://llm.liaufms.org/v1/gemma-3-12b-it
GEMMA_MODEL=google/gemma-3-12b-it
GEMMA_API_KEY=sua_chave_aqui
GEMMA_TIMEOUT_SECONDS=180
GEMMA_MAX_TOKENS=512
RAG_MODE=hibrido
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
PYTHONUNBUFFERED=1
```

### Rodar backend

```bash
python -m uvicorn web_api.main:app --reload
```

Backend local:

```text
http://127.0.0.1:8000
```

### Rodar frontend

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

## 10. Como testar

### Teste de status

```text
http://127.0.0.1:8000/api/status
```

### Teste direto da Gemma

```text
http://127.0.0.1:8000/api/debug/gemma-ping
```

### Testes no chat

```text
Responda apenas: OK
```

```text
O que é RAG?
```

```text
O que é heap?
```

```text
Monte um plano de estudos para a prova de IA.
```

```text
Gere 3 exercícios sobre embeddings.
```

```text
Inicie uma revisão ativa sobre RAG.
```

```text
Registre que tenho dificuldade em BM25.
```

---

## 11. Deploy

O projeto foi preparado para deploy com Docker.

### Hugging Face Spaces

O projeto está publicado em:

```text
https://huggingface.co/spaces/TeoZ08/jarvis-academico
```

O Space utiliza:

```yaml
sdk: docker
app_port: 7860
```

### Variáveis recomendadas no Hugging Face

Variables:

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

Secret:

```env
GEMMA_API_KEY=sua_chave_aqui
```

A chave deve ser colocada em **Secrets**, não em Variables.

---

## 12. Segurança

Arquivos e informações que não devem ser versionados:

```text
.env
GEMMA_API_KEY
HF_TOKEN
tokens pessoais
chaves privadas
```

O arquivo `.gitignore` deve impedir o envio de arquivos sensíveis.

A chave da Gemma deve ser usada apenas via:

- `.env` local; ou
- Secrets do Hugging Face.

---

## 13. Ferramentas e tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python | Backend e lógica do agente |
| FastAPI | API web |
| React | Interface web |
| Vite | Build do frontend |
| Docker | Empacotamento para deploy |
| Hugging Face Spaces | Hospedagem online |
| Render | Teste de deploy alternativo |
| OpenAI SDK | Cliente compatível com a API Gemma |
| Gemma 12B | LLM obrigatória |
| BM25 | Recuperação lexical |
| FAISS | Busca vetorial |
| Sentence Transformers | Embeddings |
| Pytest | Testes automatizados |
| Git/GitHub | Versionamento |

---

## 14. Estrutura de pastas

```text
jarvis-academico/
├── data/
├── docs/
├── frontend/
│   └── src/
├── logs/
├── scripts/
├── src/
├── storage/
├── tests/
├── web_api/
├── Dockerfile
├── README.md
├── requirements.txt
├── requirements_cpu.txt
└── render.yaml
```

---

## 15. Limitações conhecidas

- A qualidade das respostas depende dos documentos cadastrados.
- Quando o tema não existe no dataset, o sistema usa fallback acadêmico.
- Deploys gratuitos podem ter limitações de memória e tempo de resposta.
- A chave da Gemma deve ser configurada corretamente para uso real.
- O sistema não coleta dados automaticamente da internet.
- O conjunto inicial de documentos é pequeno e serve como base demonstrativa.

---

## 16. Evidências dos critérios de avaliação

### Funcionalidade — 20%

O sistema possui interface web funcional, chat, upload de documentos, consulta a materiais, tarefas, agenda e geração de plano de estudos.

### RAG — 20%

O sistema realiza chunking, indexação, recuperação de documentos, exibição de fontes e geração de resposta com contexto.

### Tool calling — 15%

A LLM aciona ferramentas internas e as chamadas são registradas na aba de evidências técnicas.

### Avaliação + erros — 20%

O projeto possui fallback acadêmico, tratamento de erro de token, timeout, ausência de contexto e endpoint de diagnóstico da Gemma.

### Aprendizado — 15%

O assistente explica conceitos, gera exercícios e monta planos de estudo.

### Engenharia — 10%

O projeto usa separação entre frontend e backend, Docker, testes, variáveis de ambiente, documentação e deploy online.

---

## 17. Autores

Projeto desenvolvido para a disciplina de Inteligência Artificial — FACOM/UFMS.

Repositório principal:

```text
https://github.com/TeoZ08/jarvis-academico
```

Deploy:

```text
https://huggingface.co/spaces/TeoZ08/jarvis-academico
```
