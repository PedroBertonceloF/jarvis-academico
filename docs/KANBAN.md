# Kanban do projeto

Este kanban registra o estado final do JARVIS Acadêmico no momento de entrega.

## Concluído

- [x] Criar estrutura base do projeto.
- [x] Implementar backend com FastAPI.
- [x] Implementar frontend em React + Vite.
- [x] Servir o frontend pelo backend FastAPI no deploy.
- [x] Implementar RAG com chunking, BM25, embeddings, FAISS e modo híbrido.
- [x] Implementar agenda acadêmica local.
- [x] Implementar lista de tarefas.
- [x] Implementar ferramenta de planejamento de estudos.
- [x] Implementar tool calling decidido pela LLM.
- [x] Integrar Gemma 12B via API LIA/UFMS.
- [x] Manter modo mock apenas como apoio de desenvolvimento.
- [x] Implementar logs estruturados de ferramentas.
- [x] Criar painel de evidências técnicas.
- [x] Implementar upload de documentos pela interface.
- [x] Implementar fallback acadêmico transparente.
- [x] Implementar revisão ativa e registro de dificuldades.
- [x] Criar testes básicos.
- [x] Criar documentação técnica.
- [x] Rodar avaliação com 10 perguntas.
- [x] Preencher classificação das respostas como correta, parcialmente correta ou incorreta.
- [x] Revisar README final.
- [x] Realizar deploy no Hugging Face Spaces.

## Validação final antes da apresentação

- [ ] Abrir o app no Hugging Face Spaces.
- [ ] Testar `/api/status`.
- [ ] Testar `/api/debug/gemma-ping`.
- [ ] Perguntar “O que é RAG?” e verificar fontes recuperadas.
- [ ] Perguntar “O que é heap?” e verificar fallback acadêmico.
- [ ] Testar revisão ativa sobre RAG.
- [ ] Registrar uma dificuldade em BM25.
- [ ] Gerar plano de estudos para a prova de IA.
- [ ] Conferir se a aba de evidências técnicas mostra tool calling, RAG e logs.

## Melhorias futuras

- [ ] Melhorar plano de estudos com divisão automática por dia.
- [ ] Criar dashboard quantitativo de uso das ferramentas.
- [ ] Criar autenticação de usuários.
- [ ] Adicionar banco remoto para persistência multiusuário.
- [ ] Ampliar suporte a PDF com extração mais robusta de tabelas.
- [ ] Melhorar histórico de dificuldades por tema.
