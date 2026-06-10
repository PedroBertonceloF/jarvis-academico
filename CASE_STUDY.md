# Case Study — JARVIS Acadêmico

## Problema

Estudantes de Computação precisam consultar materiais, revisar conceitos, organizar tarefas e entender de onde vem uma resposta gerada por IA. Um chat genérico não resolve bem esse fluxo porque não mostra fontes, evidências ou limites do dataset.

## Público-alvo

Alunos de Computação estudando Inteligência Artificial e disciplinas relacionadas, além de avaliadores interessados em ver RAG, tool calling e governança técnica funcionando em um produto acadêmico.

## Solução

Assistente acadêmico com RAG, LLM remota OpenAI-compatible, tool calling, upload de documentos, revisão ativa, registro de dificuldades, tarefas, agenda e painel de evidências.

## Minha contribuição

A confirmar no detalhe. Pelo repositório, o projeto inclui backend FastAPI, frontend React, agente acadêmico, integração LLM/LIA, RAG, ferramentas internas, persistência local, testes, documentação técnica e deploy no Hugging Face Spaces.

## Stack

- Python
- FastAPI
- React
- Vite
- LLM remota via API LIA/UFMS
- RAG lexical/híbrido
- Docker
- Hugging Face Spaces
- Pytest

## Arquitetura

O frontend React conversa com uma API FastAPI. A API orquestra um agente acadêmico que pode chamar ferramentas internas, recuperar documentos via RAG, registrar evidências, lidar com fallback e acionar a LLM remota para gerar respostas.

## Funcionalidades principais

- Chat acadêmico.
- RAG com fontes, chunks e scores.
- Tool calling com painel de evidências.
- Upload de documentos.
- Agenda e tarefas.
- Revisão ativa.
- Registro de dificuldades.
- Fallback acadêmico quando não há contexto suficiente.
- Deploy em Hugging Face Spaces.

## Decisões técnicas

- Usar a LLM remota fornecida como modelo principal para atender ao requisito acadêmico.
- Mostrar evidências de RAG e tool calling em vez de esconder a orquestração.
- Manter fallback explícito quando o dataset não cobre a pergunta.
- Documentar limitações do dataset inicial.
- Preparar modos de recuperação para ambientes com diferentes recursos.

## Desafios

- Integrar RAG, tool calling e LLM sem perder rastreabilidade.
- Manter resposta útil mesmo quando o contexto local é insuficiente.
- Criar uma interface que sirva tanto ao aluno quanto à avaliação técnica.
- Controlar timeouts, erros de token e indisponibilidade da API.

## Resultado atual

Projeto acadêmico forte com documentação, testes, frontend, backend, deploy e narrativa técnica clara para portfólio.

## Demonstração

- Sistema online: https://teoz08-jarvis-academico.hf.space
- Hugging Face Spaces: https://huggingface.co/spaces/TeoZ08/jarvis-academico
- GitHub: https://github.com/TeoZ08/jarvis-academico

## Próximos passos

- Ampliar dataset com materiais oficiais quando permitido.
- Melhorar avaliação quantitativa das respostas.
- Evoluir persistência e autenticação se virar produto multiusuário.
- Refinar UX de upload e revisão ativa.

## Como este projeto entra no portfólio

Projeto principal de IA aplicada, com profundidade técnica em RAG, agentes, tool calling, avaliação, fallback, frontend e deploy.
