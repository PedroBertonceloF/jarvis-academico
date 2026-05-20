# Análise de erros e decisões de correção

Este documento registra falhas encontradas durante o desenvolvimento do JARVIS Acadêmico e as soluções aplicadas. Ele existe para demonstrar avaliação, tratamento de erros e maturidade de engenharia.

---

## 1. Falha: resposta vazia quando o tema não estava nos materiais

### Sintoma

Perguntas sobre temas fora da base local, como `heap`, retornavam resposta insuficiente ou negativa, mesmo sendo temas acadêmicos relevantes.

### Causa

O RAG estava sendo tratado como única fonte possível de resposta. Quando a recuperação não encontrava documentos relevantes, o assistente ficava limitado.

### Correção

Foi criado o padrão **Fallback Acadêmico com Governança**:

1. o sistema tenta buscar nos materiais;
2. se não houver evidência suficiente, retorna `resultado_vazio`;
3. a resposta começa com um aviso explícito;
4. o modelo usa conhecimento geral para ajudar o aluno;
5. a interface sinaliza que houve fallback.

### Resultado

O aluno não fica sem resposta, mas também não é induzido a acreditar que a informação veio dos documentos locais.

---

## 2. Falha: deploy no Render excedendo memória

### Sintoma

O serviço no Render retornava erro HTTP 502 e foi reiniciado automaticamente por limite de memória.

### Causa

O stack de IA local é pesado para planos gratuitos:

- `torch`;
- `sentence-transformers`;
- modelo de embeddings;
- FAISS;
- indexação em memória.

### Correção

Foi previsto o uso de `RAG_MODE=lexical` em ambientes mais restritos e `RAG_MODE=hibrido` em ambientes com mais memória.

### Resultado

A arquitetura ficou adaptável ao ambiente de deploy.

---

## 3. Falha: API key inválida no Hugging Face

### Sintoma

A aplicação retornou:

```text
401 Invalid API token
```

### Causa

A chave da API foi inserida com aspas no campo Secret. Em código Python, aspas delimitam string; no painel de Secrets, elas viram parte do valor.

### Correção

A secret `GEMMA_API_KEY` foi recriada sem aspas, sem prefixo `GEMMA_API_KEY=` e sem espaços extras.

### Resultado

O erro 401 foi eliminado.

---

## 4. Falha: timeout na chamada da Gemma

### Sintoma

A aplicação retornava:

```text
Request timed out.
```

### Causa

O tempo de resposta da LLM poderia exceder o limite configurado no cliente.

### Correção

Foram adicionadas variáveis configuráveis:

```env
GEMMA_TIMEOUT_SECONDS=180
GEMMA_MAX_TOKENS=512
```

Também foi criado o endpoint:

```text
/api/debug/gemma-ping
```

para testar a Gemma sem RAG e sem tool calling.

### Resultado

O teste retornou `OK`, provando que o Hugging Face conseguia acessar a API Gemma.

---

## 5. Falha: logs técnicos pouco legíveis

### Sintoma

A aba de logs exibia apenas JSON bruto, dificultando a avaliação visual do requisito de tool calling.

### Causa

O log era útil para auditoria, mas pouco didático para apresentação.

### Correção

Foi criada uma interface de **Evidências Técnicas**, com:

- ferramenta chamada;
- entrada principal;
- método usado;
- top-k;
- melhor score;
- documentos recuperados;
- fallback tratado;
- JSON bruto recolhido em accordion.

### Resultado

A evidência técnica ficou mais clara para avaliação.

---

## 6. Falha: clipe de anexar arquivos sem ação

### Sintoma

O botão de clipe no composer do chat não executava upload.

### Causa

O botão existia visualmente, mas não estava conectado a um input de arquivo.

### Correção

Foi adicionado um input oculto com suporte a múltiplos arquivos e integração com o endpoint `/api/upload`.

### Resultado

Agora é possível anexar materiais diretamente pelo chat e reindexar a base RAG.

---

## 7. Falha: logo sobreposta no menu recolhido

### Sintoma

Ao fechar o menu lateral esquerdo, a logo e o botão de menu ficavam visualmente sobrepostos.

### Causa

O layout recolhido mantinha a distribuição horizontal do menu aberto.

### Correção

O estado recolhido passou a organizar a logo e o botão verticalmente, centralizados.

### Resultado

O menu recolhido ficou limpo e responsivo.
