# Dataset do JARVIS Acadêmico

## Origem dos dados

A versão inicial do dataset do JARVIS Acadêmico foi criada por nós em formato Markdown.

Nós elaboramos esses documentos com base no nosso entendimento dos conteúdos trabalhados ao longo da disciplina de Inteligência Artificial, nas atividades práticas desenvolvidas, nas discussões realizadas em aula e nos temas necessários para implementar o trabalho prático.

Os conteúdos foram organizados para cobrir os principais tópicos utilizados pelo sistema, incluindo:

- RAG;
- BM25;
- embeddings;
- FAISS;
- KNN;
- normalização;
- gradiente descendente;
- regressão linear;
- regressão logística;
- tool calling.

Como não tivemos uma base única de slides oficiais para todos esses tópicos, os textos do dataset inicial não devem ser interpretados como material oficial da disciplina. Eles representam uma base acadêmica inicial, produzida por nós, para permitir a implementação, teste e avaliação do mecanismo de RAG do JARVIS.

Além dessa base inicial, o sistema permite importar novos documentos, como arquivos `.pdf`, `.txt` e `.md`. Esses arquivos são processados, divididos em chunks e incorporados ao mecanismo de recuperação.

## Tipo de conteúdo

- Textos curtos explicativos em Markdown.
- Conteúdo acadêmico introdutório.
- Materiais produzidos por nós com base no entendimento das aulas e atividades.
- Temas alinhados ao trabalho prático e aos conceitos estudados na disciplina.

## Limitações

- Os textos são sintéticos e resumidos.
- Os documentos iniciais não substituem bibliografia oficial, livros, artigos ou materiais completos do professor.
- Algumas definições podem ser mais gerais, pois foram produzidas com base no nosso entendimento.
- Perguntas muito específicas podem não ter resposta suficiente no contexto.
- A qualidade das respostas depende diretamente da qualidade e abrangência dos documentos cadastrados.

## Estratégia de chunking

O sistema usa chunking por parágrafos, com limite aproximado de 700 caracteres e sobreposição de 80 caracteres quando o texto é maior que esse limite.

Escolhemos essa estratégia para manter os trechos pequenos o suficiente para uma recuperação eficiente, mas ainda com contexto suficiente para que a LLM consiga gerar respostas úteis.

## Impacto no RAG

Os chunks médios ajudam a preservar contexto sem deixar os trechos longos demais. A sobreposição reduz o risco de cortar uma explicação importante entre dois chunks.

Para documentos maiores, como PDFs, apostilas ou anotações completas, pode ser necessário testar diferentes tamanhos de chunk e comparar o impacto na qualidade das respostas.

## Observação sobre governança dos dados

O JARVIS Acadêmico não coleta dados automaticamente da internet. A base de conhecimento é formada por documentos locais cadastrados no projeto e por materiais adicionados manualmente pelo usuário.

Essa escolha permite maior controle sobre a origem dos dados, facilita a análise das respostas geradas e torna o funcionamento do RAG mais transparente.

## Política de ingestão: contexto vs. conexões

Regra de decisão sobre o que pode entrar no índice de recuperação (`/data`):

- **Contexto (indexar)** — apenas material acadêmico *perene*: conceitos, teoria,
  apostilas, definições que continuarão úteis daqui a um ano. É isso que pertence a
  `/data` e é chunkado/vetorizado.
- **Conexões (NÃO indexar)** — dados voláteis e mutáveis: tarefas, agenda,
  dificuldades e revisões. Já vivem em `/storage` como JSON e devem ser consultados
  ao vivo pelas ferramentas do agente, nunca vetorizados. Vetorizar dado volátil
  gera ruído e exige limpeza recorrente.
- **Teste do perene:** antes de colocar um arquivo em `/data`, pergunte *"isto ainda
  vai importar daqui a um ano?"*. Se não, mantenha fora do índice.
- **Dados pessoais de terceiros (LGPD):** trabalhos, provas ou documentos de outras
  pessoas enviados via `/data/uploads` podem conter dados pessoais. Não os trate como
  material perene da base e não os exponha em respostas sem necessidade. Ao processar
  via LLM remota (LIA/UFMS), lembre que o conteúdo sai da máquina — anonimize quando
  o dado for de terceiros. Ver `../../SECOND-BRAIN.md` (gate de governança, tier T2).
