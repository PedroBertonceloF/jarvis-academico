# PRD — JARVIS Acadêmico

## Objetivo
Desenvolver um assistente acadêmico capaz de apoiar estudantes na organização dos estudos usando RAG, tool calling e a LLM Gemma 12B via API.

## Público-alvo
Estudantes que precisam consultar materiais, organizar agenda, controlar tarefas e planejar revisões.

## Funcionalidades obrigatórias
- Consulta a materiais de estudo usando RAG.
- Consulta de agenda acadêmica.
- Lista de tarefas com adição, listagem e conclusão.
- Planejamento de estudos combinando agenda, tarefas e materiais.
- Tool calling decidido pela LLM.
- Logs das ferramentas chamadas, com entrada e saída.
- Funcionalidades de aprendizado, incluindo geração de exercícios e active recall.
- Avaliação com 10 perguntas e análise de erros.

## Fora de escopo
- Autenticação de usuários.
- Banco de dados remoto.
- Deploy público em produção.
- Uso ilimitado da API Gemma.
- Multiusuário com controle de permissões.

## Critérios de sucesso
- O sistema executa de ponta a ponta no modo mock e no modo Gemma.
- As ferramentas são chamadas pela LLM e registradas em log.
- O RAG recupera documentos relevantes e responde com base nos trechos.
- A entrega contém documentação, testes básicos, avaliação e análise de erros.


## Melhoria implementada

O sistema permite que o usuário importe materiais acadêmicos diretamente pela interface Streamlit. Os arquivos são persistidos em `data/uploads/` e passam a compor a base de conhecimento após a reindexação.

## Requisito adicional: fallback acadêmico transparente

Quando a pergunta do usuário for acadêmica, mas não houver evidência suficiente nos materiais cadastrados, o JARVIS deve:

1. indicar claramente que o tema não foi encontrado nos materiais;
2. responder usando conhecimento geral da LLM;
3. sugerir que o aluno importe material sobre o tema para respostas futuras baseadas em RAG.

Esse requisito torna o sistema mais útil como tutor sem comprometer a transparência sobre a origem da informação.
