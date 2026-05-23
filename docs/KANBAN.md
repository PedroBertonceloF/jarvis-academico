# Kanban do projeto

## Concluído

- [x] Criar estrutura base do projeto.
- [x] Implementar RAG com chunking, BM25, embeddings e FAISS.
- [x] Implementar agenda local em JSON.
- [x] Implementar lista de tarefas.
- [x] Implementar ferramenta de planejamento de estudos.
- [x] Implementar tool calling decidido pela LLM.
- [x] Implementar logs de ferramentas.
- [x] Migrar interface final para React + FastAPI.
- [x] Implementar upload de documentos pela interface web.
- [x] Implementar fallback acadêmico transparente.
- [x] Implementar revisão ativa.
- [x] Implementar registro de dificuldades.
- [x] Criar endpoints de diagnóstico da Gemma.
- [x] Criar testes básicos.
- [x] Criar documentação técnica.
- [x] Preencher avaliação com 10 perguntas.
- [x] Configurar deploy no Hugging Face Spaces.
- [x] Sincronizar GitHub e Hugging Face.

---

## Validação final

- [ ] Conferir `git status` limpo.
- [ ] Conferir YAML do Hugging Face no topo do `README.md`.
- [ ] Conferir deploy em `https://teoz08-jarvis-academico.hf.space`.
- [ ] Testar `/api/status`.
- [ ] Testar `/api/debug/gemma-ping`.
- [ ] Testar fluxo de chat, RAG, revisão ativa, dificuldade e plano de estudos.
- [ ] Gravar pitch/vídeo de 3 minutos.

---

## Melhorias futuras

- [ ] Ampliar dataset com materiais reais adicionais da disciplina.
- [ ] Adicionar métricas quantitativas mais completas para avaliação do RAG.
- [ ] Melhorar plano de estudos com divisão automática por dia.
- [ ] Criar exportação de evidências em PDF ou Markdown.
- [ ] Melhorar histórico de dificuldades por tópico.
