# Decisões técnicas

## 1. Uso de Streamlit
Streamlit foi escolhido por permitir criar uma interface funcional rapidamente, com baixo custo de implementação e boa demonstração no vídeo.

## 2. Modo mock
O modo mock permite desenvolver e testar o fluxo sem consumir tokens da API Gemma do LIA. A entrega final deve validar o funcionamento com `LLM_MODE=gemma`.

## 3. RAG híbrido
O RAG usa BM25 para busca lexical e FAISS com embeddings para busca semântica. A busca híbrida combina as duas pontuações para reduzir falhas quando a pergunta usa termos diferentes dos documentos.

## 4. Chunking
A versão otimizada usa chunks de aproximadamente 700 caracteres com sobreposição de 80. Essa escolha reduz consumo de tokens e preserva contexto suficiente para respostas curtas.

## 5. Tool calling
A decisão de chamada é feita pela LLM. O Python apenas executa a ferramenta solicitada e registra entrada/saída no log.

## 6. Segurança
A chave da API fica no `.env`, que está no `.gitignore`. O arquivo `.env.example` contém apenas placeholders.

## 7. Testes
Foram incluídos testes básicos para chunking e armazenamento. O objetivo é demonstrar engenharia mínima e reduzir risco de quebra em pontos centrais.
