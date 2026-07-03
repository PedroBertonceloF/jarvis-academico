# Embeddings

Embeddings são representações vetoriais densas de textos. A ideia é transformar frases, parágrafos ou documentos em vetores numéricos que capturam similaridade semântica. Textos com significados parecidos tendem a ficar próximos no espaço vetorial.

Diferentemente de representações esparsas, como TF-IDF, embeddings não dependem apenas da presença exata de palavras. Eles permitem recuperar conteúdos semanticamente relacionados mesmo quando a consulta usa palavras diferentes do documento.

Em RAG, embeddings são usados para busca densa. O usuário envia uma pergunta, a pergunta é convertida em vetor, e o sistema recupera os chunks com maior similaridade. Uma medida comum é a similaridade de cosseno.

## Diferença entre embeddings e BM25

A diferença entre embeddings e BM25 é o tipo de correspondência. Embeddings comparam significado (busca densa/semântica), enquanto o BM25 compara termos exatos (busca lexical). Por isso os embeddings recuperam conteúdo relevante mesmo quando a pergunta usa palavras diferentes do documento, situação em que o BM25 tende a falhar. Muitos sistemas de RAG usam recuperação híbrida, combinando os scores de BM25 e de embeddings.
