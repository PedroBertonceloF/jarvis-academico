# FAISS

FAISS é uma biblioteca para busca eficiente em vetores. Em aplicações de RAG, ela permite armazenar embeddings dos chunks e recuperar rapidamente os vetores mais próximos do vetor da pergunta.

Quando os embeddings são normalizados, o produto interno pode ser usado como aproximação da similaridade de cosseno. Isso facilita a busca por similaridade semântica.

FAISS é útil porque uma busca ingênua comparando uma pergunta com todos os documentos pode ficar lenta quando a base cresce. Com índices vetoriais, o sistema fica mais escalável e adequado para bases maiores.
