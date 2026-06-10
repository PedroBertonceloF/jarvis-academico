# PRD — JARVIS Acadêmico

## Objetivo

Desenvolver um assistente acadêmico capaz de apoiar estudantes na organização dos estudos usando **RAG**, **tool calling** e uma **LLM remota OpenAI-compatible via API LIA/UFMS**.

---

## Público-alvo

Estudantes que precisam consultar materiais, organizar agenda, controlar tarefas, planejar revisões e praticar conceitos acadêmicos.

---

## Funcionalidades obrigatórias

- Consulta a materiais de estudo usando RAG.
- Consulta de agenda acadêmica.
- Lista de tarefas com adição, listagem e conclusão.
- Planejamento de estudos combinando agenda, tarefas, materiais e dificuldades.
- Tool calling decidido pela LLM.
- Logs das ferramentas chamadas, com entrada e saída.
- Funcionalidades de aprendizado, incluindo exercícios, revisão ativa e registro de dificuldades.
- Avaliação do sistema com 10 perguntas.
- Análise de erros e limitações.

---

## Funcionalidades implementadas

### Chat acadêmico

O usuário conversa com o JARVIS sobre conteúdos da disciplina de Inteligência Artificial e temas gerais de Computação.

### RAG

O sistema recupera trechos relevantes dos documentos cadastrados, mostra fontes e usa esses trechos para orientar a resposta da LLM.

### Upload de documentos

O sistema permite importar materiais acadêmicos pela interface web React. Os arquivos são enviados para o backend FastAPI, persistidos em `data/uploads/` e incorporados à base de conhecimento após a reindexação.

Formatos previstos:

- `.pdf`;
- `.txt`;
- `.md`;
- `.py`.

### Agenda e tarefas

O sistema permite consultar e registrar compromissos acadêmicos, tarefas e prazos.

### Planejamento de estudos

O plano considera materiais, agenda, tarefas e dificuldades registradas.

### Revisão ativa

O sistema gera uma pergunta de revisão, recebe a resposta do aluno e avalia a resposta com feedback objetivo.

### Registro de dificuldades

O usuário pode registrar dificuldades manualmente, e o sistema também pode registrar dificuldades a partir de respostas parciais ou incorretas em revisão ativa.

---

## Requisito adicional: fallback acadêmico transparente

Quando a pergunta do usuário for acadêmica, mas não houver evidência suficiente nos materiais cadastrados, o JARVIS deve:

1. indicar claramente que o tema não foi encontrado nos materiais;
2. responder usando conhecimento geral da LLM;
3. sugerir que o aluno importe material sobre o tema para respostas futuras baseadas em RAG.

Esse requisito torna o sistema mais útil como tutor sem comprometer a transparência sobre a origem da informação.

---

## Fora de escopo

- Autenticação de usuários.
- Banco de dados remoto.
- Multiusuário com controle de permissões.
- Coleta automática de dados da internet.
- Uso ilimitado da API LLM.

---

## Critérios de sucesso

- O sistema executa de ponta a ponta no modo remoto (`LLM_MODE=gemma` legado ou `LLM_MODE=qwen`).
- O deploy oficial roda no Hugging Face Spaces.
- As ferramentas são chamadas pela LLM e registradas em log.
- O RAG recupera documentos relevantes e apresenta fontes.
- O fallback acadêmico é transparente quando não há evidência suficiente.
- A entrega contém documentação, testes básicos, avaliação com 10 perguntas e análise de erros.
