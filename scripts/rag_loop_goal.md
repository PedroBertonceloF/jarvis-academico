# /goal — Loop de verificação da recuperação (RAG)

GOAL
Melhorar a qualidade da recuperação do RAG do JARVIS Acadêmico, medida por um
harness objetivo, sem regressões nos testes.

VERIFICATION (a cada iteração, RODE ISTO — não confie em opinião)
- Configuração real (híbrido): `LLM_MODE=mock python scripts/eval_rag.py`
- Baseline leve (BM25):        `RAG_MODE=lexical LLM_MODE=mock python scripts/eval_rag.py`
- Regressão geral:             `python -m pytest -q`
Leia o exit code e as linhas `recall@k`, `MRR`, `secundárias faltando`.

DONE (pare quando TUDO for verdadeiro no modo híbrido)
- recall@3 == 1.00 (10/10) — não pode cair; e
- MRR >= 0.95 (a fonte esperada deve tender ao rank 1); e
- "secundárias faltando" == 0 (cobrir embeddings na pergunta BM25 vs embeddings); e
- `pytest` continua 100% verde.

HARD STOP
- Máximo de 6 passes. Se não atingir DONE em 6, PARE e reporte o melhor estado
  alcançado + o que travou. Não fique iterando indefinidamente.

LOOP (reason -> act -> observe)
1. REASON: rode a verificação, leia a métrica, identifique a MENOR mudança que
   provavelmente melhora o ponto mais fraco (hoje: Q2/embeddings e alguns rank=2/3).
2. ACT: aplique UMA mudança por vez. Alavancas permitidas, da mais barata p/ mais cara:
   - ajustar `RagConfig` em src/rag.py (tamanho_chunk, sobreposicao, alpha_hibrido,
     min_score_dense, min_sobreposicao_termos);
   - melhorar/expandir o dataset em data/ (ex.: um doc dedicado a embeddings, ou
     enriquecer 03_embeddings.md para casar com a pergunta comparativa);
   - por último, mexer na estratégia de recuperação/reranking.
3. OBSERVE: rode a verificação de novo. Registre num log a mudança e o delta da métrica.
4. Repita até DONE ou HARD STOP.

GUARDRAILS
- NÃO edite scripts/eval_rag.py nem docs/AVALIACAO_10_PERGUNTAS.md para "passar" —
  isso é fraudar o teste. O gabarito é fixo.
- Cuidado com overfitting: se você editar o dataset, as 10 perguntas não são o
  universo — mudanças devem fazer sentido acadêmico, não decorar o gabarito.
- Uma mudança por iteração; se uma mudança piorar a métrica, reverta antes de tentar outra.
- Não faça commit sem me perguntar. Ao final, mostre o diff e um resumo do log.
- Custo: cada pass é barato (recuperação, sem LLM). Não gaste passes à toa.
