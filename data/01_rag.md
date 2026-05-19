# RAG — Retrieval-Augmented Generation

RAG é uma arquitetura que combina recuperação de informação com geração de texto. Primeiro, o sistema busca documentos ou trechos relevantes em uma base de conhecimento. Depois, esses trechos são enviados para uma LLM, que produz uma resposta fundamentada no contexto recuperado.

O objetivo principal é reduzir alucinações. Em vez de depender apenas do conhecimento interno do modelo, a resposta passa a ser ancorada em evidências externas. Um pipeline básico de RAG possui cinco etapas: carregamento de documentos, chunking, geração de embeddings, recuperação dos trechos mais relevantes e geração da resposta pela LLM.

A qualidade do RAG depende muito da qualidade dos documentos, do tamanho dos chunks, do método de busca e do prompt. Chunks muito pequenos podem perder contexto. Chunks muito longos podem diluir a informação importante. Por isso, uma estratégia comum é usar chunks de tamanho médio com sobreposição.
