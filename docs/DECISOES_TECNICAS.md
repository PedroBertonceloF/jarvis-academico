# Decisões técnicas

## 1. React como interface final

A interface final foi construída em React para melhorar:

- apresentação;
- responsividade;
- organização das telas;
- experiência de chat;
- painel de evidências;
- possibilidade de evoluir o projeto como portfólio.

---

## 2. FastAPI como backend

FastAPI foi escolhido por ser leve, direto e compatível com deploy Docker.

Benefícios:

- endpoints REST claros;
- integração simples com frontend;
- documentação automática;
- boa performance;
- facilidade para upload e diagnóstico.

---

## 3. Docker como padrão de deploy

O Docker evita diferenças entre máquinas e ambientes de hospedagem.

O mesmo projeto pode ser executado em:

- máquina local;
- Hugging Face Spaces;
- VPS futura.

---

## 4. Variáveis de ambiente

Configurações sensíveis foram isoladas:

```env
GEMMA_API_KEY
GEMMA_BASE_URL
GEMMA_MODEL
LLM_MODE
RAG_MODE
```

Isso evita vazar chaves no GitHub e permite trocar modos sem alterar código.

---

## 5. RAG híbrido e modo lexical

O projeto suporta busca híbrida, mas também possui modo lexical.

Motivo:

- busca híbrida é mais robusta semanticamente;
- busca lexical é mais leve para ambientes com pouca memória.

Essa decisão permite adaptar o sistema ao ambiente sem remover funcionalidade.

---

## 6. Fallback acadêmico com transparência

Quando o RAG não encontra evidência suficiente, o sistema não inventa fonte.

Ele informa que não encontrou o tema nos materiais e só então usa conhecimento geral do modelo.

Essa decisão melhora:

- confiabilidade;
- transparência;
- experiência do aluno;
- análise de erros.

---

## 7. Logs estruturados

Cada chamada de ferramenta gera um log com entrada e saída.

Motivo:

- demonstrar tool calling;
- facilitar debug;
- fornecer evidência para avaliação;
- permitir auditoria técnica.

---

## 8. Endpoint de diagnóstico da Gemma

Foi criado:

```text
/api/debug/gemma-ping
```

Motivo:

- isolar erro de API key;
- diagnosticar timeout;
- confirmar conectividade da hospedagem com a API LIA/UFMS;
- separar problema da LLM de problema do agente/RAG.

---

## 9. Upload pelo chat e pelo painel de materiais

O upload foi mantido no painel de materiais e também conectado ao clipe do composer.

Motivo:

- tornar a interação mais natural;
- reduzir atrito para anexar PDF ou anotação;
- deixar a aplicação mais próxima de um assistente real.

---

## 10. Painel de evidências em vez de JSON bruto

O JSON bruto continua disponível, mas a tela principal exibe dados interpretados.

Motivo:

- facilitar correção;
- destacar requisitos do trabalho;
- demonstrar RAG, tool calling e fallback de forma clara.
