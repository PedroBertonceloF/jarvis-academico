# PRD — JARVIS Acadêmico

## Objetivo

Desenvolver um assistente acadêmico capaz de apoiar estudantes na organização dos estudos usando RAG, tool calling e a LLM Gemma 12B via API LIA/UFMS.

## Público-alvo

Estudantes que precisam consultar materiais, organizar agenda, controlar tarefas, revisar conteúdos e planejar estudos.

## Funcionalidades obrigatórias

- Consulta a materiais de estudo usando RAG.
- Consulta de agenda acadêmica.
- Lista de tarefas com adição, listagem e conclusão.
- Planejamento de estudos combinando agenda, tarefas e materiais.
- Tool calling decidido pela LLM.
- Logs das ferramentas chamadas, com entrada e saída.
- Avaliação com 10 perguntas.
- Análise de erros e decisões de correção.

## Funcionalidades adicionais implementadas

- Interface web em React + Vite.
- Backend FastAPI.
- Deploy com Docker no Hugging Face Spaces.
- Upload de documentos pela interface.
- Reindexação da base após upload.
- Fallback acadêmico transparente para temas fora dos materiais.
- Revisão ativa sobre temas acadêmicos.
- Registro de dificuldades do aluno.
- Plano de estudos considerando agenda, tarefas, materiais e dificuldades.
- Endpoints de diagnóstico para configuração e Gemma.
- Painel de evidências técnicas para demonstrar RAG, tool calling e logs.

## Fora de escopo

- Autenticação de usuários.
- Banco de dados remoto.
- Multiusuário com controle de permissões.
- Coleta automática de dados da internet.
- Uso ilimitado da API Gemma.
- Garantia de produção comercial.

## Critérios de sucesso

- O sistema executa de ponta a ponta no modo Gemma.
- O modo mock continua disponível apenas como apoio de desenvolvimento.
- As ferramentas são chamadas pela LLM e registradas em log.
- O RAG recupera documentos relevantes e responde com base nos trechos.
- A interface exibe fontes, ferramentas chamadas e evidências técnicas.
- A entrega contém documentação, testes básicos, avaliação e análise de erros.
- O deploy oficial no Hugging Face Spaces está acessível para teste.

## Upload de materiais

O sistema permite que o usuário importe materiais acadêmicos diretamente pela interface web. Os arquivos são persistidos em `data/uploads/` e passam a compor a base de conhecimento após a reindexação.

Esse recurso permite ampliar a base do RAG sem alterar manualmente os arquivos internos do projeto.

## Fallback acadêmico transparente

Quando a pergunta do usuário for acadêmica, mas não houver evidência suficiente nos materiais cadastrados, o JARVIS deve:

1. indicar claramente que o tema não foi encontrado nos materiais;
2. responder usando conhecimento geral da LLM;
3. sugerir que o aluno importe material sobre o tema para respostas futuras baseadas em RAG.

Esse requisito torna o sistema mais útil como tutor sem comprometer a transparência sobre a origem da informação.

## Aprendizado e revisão ativa

O sistema também apoia o aprendizado por meio de:

- geração de perguntas de revisão;
- avaliação de respostas do aluno;
- registro de dificuldades;
- uso das dificuldades no planejamento de estudos.

Essa camada reforça o papel do JARVIS como assistente acadêmico, não apenas como chat de perguntas e respostas.
