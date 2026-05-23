# Avaliação do Sistema — 10 Perguntas

Este documento registra uma avaliação manual do JARVIS Acadêmico com 10 perguntas relacionadas aos conteúdos da disciplina e aos requisitos do trabalho.

Critérios usados na classificação:

- **Correta**: a resposta atende ao que foi perguntado, com base adequada nos materiais recuperados.
- **Parcialmente correta**: a resposta acerta parte importante, mas deixa algum ponto relevante incompleto.
- **Incorreta**: a resposta não responde adequadamente ou apresenta informação incompatível com os materiais.

## Resumo da avaliação

| Classificação | Quantidade |
|---|---:|
| Corretas | 9 |
| Parcialmente corretas | 1 |
| Incorretas | 0 |
| Total | 10 |

Resultado geral: o sistema apresentou bom desempenho nas perguntas de avaliação. A principal limitação observada ocorreu na comparação entre BM25 e embeddings, em que a recuperação trouxe bons trechos sobre BM25, mas não trouxe evidência suficiente sobre embeddings.

---

## 1. O que é RAG?

**Documentos recuperados:**

- `01_rag_chunk_0000` — `01_rag.md`, score `0.9892`
- `03_embeddings_chunk_0001` — `03_embeddings.md`, score `0.7578`
- `04_faiss_chunk_0000` — `04_faiss.md`, score `0.6843`

**Resposta resumida:**

RAG (Retrieval-Augmented Generation) é uma arquitetura que combina recuperação de informação com geração de texto. O sistema busca documentos ou trechos relevantes em uma base de conhecimento e envia esses trechos para uma LLM, que gera uma resposta baseada no contexto recuperado. O objetivo principal é reduzir alucinações, ancorando a resposta em evidências externas.

**Classificação:** Correta.

**Observação:** A resposta explicou corretamente que RAG combina recuperação de documentos com geração por LLM e destacou a redução de alucinações com base em contexto externo.

---

## 2. Qual a diferença entre BM25 e embeddings?

**Documentos recuperados:**

- `02_bm25_chunk_0000` — `02_bm25.md`, score `0.8763`
- `10_tool_calling_chunk_0001` — `10_tool_calling.md`, score `0.6455`
- `02_bm25_chunk_0001` — `02_bm25.md`, score `0.6394`

**Resposta resumida:**

A resposta informou que não encontrou evidências suficientes para comparar BM25 e embeddings. Explicou que BM25 é um método de recuperação lexical baseado na frequência dos termos da consulta nos documentos, com ajustes para repetição de palavras e tamanho do documento. Também mencionou que BM25 pode ter dificuldade quando o usuário usa sinônimos ou formula a pergunta de modo semanticamente diferente. Porém, não comparou embeddings por falta de evidência recuperada.

**Classificação:** Parcialmente correta.

**Observação:** A resposta explicou bem o BM25, mas não comparou embeddings porque os documentos recuperados não trouxeram evidência suficiente sobre esse segundo conceito. Isso indica uma limitação pontual de recuperação/contexto.

---

## 3. Por que fazer chunking?

**Documentos recuperados:**

- `README_DATASET_chunk_0003` — `README_DATASET.md`, score `1.0000`
- `01_rag_chunk_0000` — `01_rag.md`, score `0.5583`
- `01_rag_chunk_0001` — `01_rag.md`, score `0.5407`

**Resposta resumida:**

O chunking é feito para manter os trechos pequenos o suficiente para uma recuperação eficiente, mas ainda com contexto suficiente para que a LLM consiga gerar respostas úteis. A sobreposição entre chunks reduz o risco de cortar uma explicação importante entre dois trechos. Chunks muito pequenos podem perder contexto; chunks muito longos podem diluir a informação importante.

**Classificação:** Correta.

**Observação:** A resposta justificou corretamente o chunking como estratégia para manter trechos recuperáveis, preservar contexto e reduzir cortes de explicações importantes.

---

## 4. O que é FAISS?

**Documentos recuperados:**

- `04_faiss_chunk_0000` — `04_faiss.md`, score `1.0000`
- `09_regressao_logistica_chunk_0000` — `09_regressao_logistica.md`, score `0.6061`
- `01_rag_chunk_0000` — `01_rag.md`, score `0.5675`

**Resposta resumida:**

FAISS é uma biblioteca para busca eficiente em vetores. Em aplicações de RAG, permite armazenar embeddings dos chunks e recuperar rapidamente os vetores mais próximos do vetor da pergunta. Isso torna o sistema mais escalável e adequado para bases de conhecimento maiores.

**Classificação:** Correta.

**Observação:** A resposta definiu FAISS corretamente como biblioteca de busca vetorial eficiente e relacionou seu uso com embeddings e escalabilidade em RAG.

---

## 5. O que é KNN?

**Documentos recuperados:**

- `05_knn_chunk_0000` — `05_knn.md`, score `0.9652`
- `06_normalizacao_knn_chunk_0000` — `06_normalizacao_knn.md`, score `0.7672`
- `10_tool_calling_chunk_0000` — `10_tool_calling.md`, score `0.5840`

**Resposta resumida:**

KNN é um algoritmo de aprendizado baseado em instâncias. Durante o treinamento, armazena os exemplos. Para classificar um novo exemplo, calcula a distância entre ele e os exemplos armazenados. Na classificação, retorna a classe mais frequente entre os k vizinhos mais próximos; na regressão, retorna a média dos valores dos k vizinhos.

**Classificação:** Correta.

**Observação:** A resposta explicou corretamente KNN como algoritmo baseado em instâncias, incluindo classificação por maioria dos k vizinhos e regressão por média dos vizinhos.

---

## 6. Por que normalizar atributos no KNN?

**Documentos recuperados:**

- `06_normalizacao_knn_chunk_0000` — `06_normalizacao_knn.md`, score `1.0000`
- `05_knn_chunk_0000` — `05_knn.md`, score `0.6157`
- `09_regressao_logistica_chunk_0000` — `09_regressao_logistica.md`, score `0.3562`

**Resposta resumida:**

A normalização é importante porque o KNN depende de medidas de distância. Se um atributo tiver escala muito maior que os demais, ele pode dominar o cálculo da distância e prejudicar a classificação. Uma estratégia comum é a normalização min-max, que transforma valores para o intervalo entre 0 e 1.

**Classificação:** Correta.

**Observação:** A resposta explicou corretamente que a normalização evita que atributos em escala maior dominem a distância no KNN e citou min-max como estratégia.

---

## 7. Para que serve a função sigmoide?

**Documentos recuperados:**

- `09_regressao_logistica_chunk_0000` — `09_regressao_logistica.md`, score `1.0000`
- `07_gradiente_descendente_chunk_0000` — `07_gradiente_descendente.md`, score `0.7058`
- `08_regressao_linear_chunk_0000` — `08_regressao_linear.md`, score `0.6344`

**Resposta resumida:**

A função sigmoide, utilizada na regressão logística, transforma uma combinação linear dos atributos em um valor entre 0 e 1. Isso permite interpretar a saída como probabilidade de pertencer à classe positiva.

**Classificação:** Correta.

**Observação:** A resposta explicou corretamente a função sigmoide como transformação da saída linear em valor entre 0 e 1, interpretável como probabilidade.

---

## 8. O que é gradiente descendente?

**Documentos recuperados:**

- `07_gradiente_descendente_chunk_0000` — `07_gradiente_descendente.md`, score `1.0000`
- `08_regressao_linear_chunk_0001` — `08_regressao_linear.md`, score `0.8599`
- `07_gradiente_descendente_chunk_0001` — `07_gradiente_descendente.md`, score `0.6877`

**Resposta resumida:**

Gradiente descendente é um método de otimização usado para minimizar uma função de custo. Ele ajusta os parâmetros na direção oposta ao gradiente, pois o gradiente indica a direção de maior crescimento da função.

**Classificação:** Correta.

**Observação:** A resposta explicou corretamente o gradiente descendente como método de otimização que ajusta parâmetros na direção oposta ao gradiente para minimizar a função de custo.

---

## 9. Qual a diferença entre regressão linear e logística?

**Documentos recuperados:**

- `08_regressao_linear_chunk_0000` — `08_regressao_linear.md`, score `0.9922`
- `09_regressao_logistica_chunk_0000` — `09_regressao_logistica.md`, score `0.9874`
- `08_regressao_linear_chunk_0001` — `08_regressao_linear.md`, score `0.5438`

**Resposta resumida:**

Regressão linear é utilizada para prever valores contínuos, enquanto regressão logística é utilizada principalmente para classificação binária. A regressão logística usa a função sigmoide para transformar a saída em uma probabilidade entre 0 e 1.

**Classificação:** Correta.

**Observação:** A resposta comparou corretamente regressão linear e logística, diferenciando previsão de valores contínuos e classificação binária com sigmoide.

---

## 10. O que é tool calling?

**Documentos recuperados:**

- `10_tool_calling_chunk_0000` — `10_tool_calling.md`, score `1.0000`
- `README_DATASET_chunk_0000` — `README_DATASET.md`, score `0.4258`
- `01_rag_chunk_0000` — `01_rag.md`, score `0.3393`

**Resposta resumida:**

Tool calling é uma técnica em que uma LLM decide chamar ferramentas externas para resolver partes de uma tarefa. Em vez de apenas responder com texto, o modelo identifica quando precisa consultar uma agenda, buscar documentos, listar tarefas ou executar outra função do sistema. Uma implementação controlada pode pedir para a LLM retornar uma estrutura JSON com o nome da ferramenta e os argumentos necessários.

**Classificação:** Correta.

**Observação:** A resposta explicou corretamente tool calling como a capacidade da LLM de acionar ferramentas externas e citou exemplos coerentes com o sistema.

---

## Conclusão

A avaliação indica que o JARVIS Acadêmico atende ao requisito de avaliação com 10 perguntas. O único ponto parcialmente correto está relacionado à recuperação insuficiente de evidência sobre embeddings na pergunta comparativa com BM25.

Essa falha é útil para a análise de erros, pois mostra uma limitação real do pipeline de recuperação e justifica melhorias futuras no dataset, no chunking ou na estratégia de recuperação híbrida.
