# Dataset do JARVIS Acadêmico

## Origem dos dados

Esta versão inicial usa 10 documentos acadêmicos em Markdown criados para cobrir os principais temas da disciplina de Inteligência Artificial: RAG, BM25, embeddings, FAISS, KNN, normalização, gradiente descendente, regressão linear, regressão logística e tool calling.

Na entrega final, recomenda-se substituir ou complementar estes arquivos com os PDFs, anotações e materiais reais usados em aula.

## Tipo de conteúdo

- Textos curtos explicativos em Markdown.
- Conteúdo acadêmico introdutório.
- Temas alinhados ao trabalho prático e à disciplina.

## Limitações

- Os textos são sintéticos e resumidos.
- Não substituem bibliografia oficial nem materiais completos do professor.
- Algumas perguntas muito específicas podem não ter resposta suficiente no contexto.

## Estratégia de chunking

O sistema usa chunking por parágrafos com limite aproximado de 700 caracteres e sobreposição de 80 caracteres quando o texto é maior que o limite.

## Impacto no RAG

Chunks médios preservam contexto suficiente para a LLM responder sem diluir demais a informação. A sobreposição reduz o risco de cortar uma explicação importante entre dois chunks. Para PDFs longos, pode ser necessário testar tamanhos diferentes e registrar o impacto na avaliação.
