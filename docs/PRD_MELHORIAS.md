# PRD — Melhorias de Confiabilidade, Transparência do RAG e Progresso de Aprendizado

> Gerado a partir de uma revisão de estado do projeto (project-health-check) sobre o JARVIS Acadêmico. Cobre 3 blocos priorizados pelo mantenedor: confiabilidade do backend, transparência do RAG no chat, e um painel de progresso de aprendizado.

## Problem Statement

O JARVIS Acadêmico já atende a todos os requisitos do Trabalho 2 (tool calling, RAG, agenda, tarefas, revisão ativa, deploy), mas a revisão de estado identificou três pontos que limitam a confiança e a visibilidade do sistema do ponto de vista de quem usa e de quem avalia:

1. **Confiabilidade silenciosa**: `storage.py` escreve JSON sem atomicidade nem validação — uma falha no meio de uma escrita ou uma data inválida em uma tarefa/evento pode corromper dados sem aviso, e `/api/health` não diz nada sobre o estado real de RAG, LLM ou storage.
2. **RAG pouco transparente no chat**: as fontes recuperadas pelo RAG só aparecem na aba "Evidências"; na conversa principal, o aluno não vê de onde veio a informação nem o quão relevante ela foi. Além disso, um PDF corrompido na base de materiais pode interromper toda a indexação.
3. **Progresso de aprendizado invisível**: o sistema já registra dificuldades e avalia revisões ativas (`DificuldadeStore`, `RevisaoStore`), mas esses dados nunca são agregados ou mostrados ao aluno — não há como ver evolução, taxa de acerto ou temas recorrentes.

## Solution

1. Introduzir uma camada de armazenamento com escrita atômica e validação básica (`JsonCollectionStore`), e um agregador de saúde (`verificar_saude`) que reporta o estado real de RAG, LLM e storage via `/api/health`.
2. Tornar o RAG transparente: tratar erros de leitura de PDF sem derrubar a indexação, expor quais documentos falharam, e citar as fontes/scores diretamente nas respostas do chat (`fontes_citadas`), exibidas como chips inline na UI.
3. Adicionar um módulo `LearningAnalytics` que agrega dificuldades e revisões em um resumo de progresso, exposto via `/api/analytics/progresso` e exibido em uma nova aba "Progresso" no frontend.

## User Stories

1. Como aluno, quero que minhas tarefas, agenda e dificuldades não sejam corrompidas se eu enviar várias requisições ao mesmo tempo, para não perder meus dados de estudo.
2. Como aluno, quero que datas inválidas sejam rejeitadas ao adicionar eventos ou tarefas, para que minha agenda permaneça consistente.
3. Como aluno, quero que prioridades inválidas em tarefas sejam rejeitadas com uma mensagem clara, para corrigir o erro na hora.
4. Como mantenedor, quero um endpoint `/api/health` que reporte o status real de RAG, LLM e storage, para diagnosticar problemas rapidamente em produção (Hugging Face Spaces).
5. Como avaliador do trabalho, quero ver em `/api/health` se o sistema está saudável antes de avaliar a demo, para confiar que o sistema está funcionando.
6. Como mantenedor, quero que `/api/health` funcione em `LLM_MODE=mock`, sem exigir token configurado, para rodar a checagem localmente.
7. Como mantenedor, quero que `/api/health` não chame a LLM remota por padrão (apenas com `?verbose=true`), para não gerar custo/latência a cada checagem.
8. Como aluno, quero que um PDF corrompido na minha base de materiais não impeça o RAG de indexar os outros documentos, para que minha base continue funcional.
9. Como aluno, quero ver em `/api/status` quais documentos falharam ao ser indexados, para saber quais arquivos preciso substituir.
10. Como aluno, quero ver as fontes citadas diretamente abaixo da resposta do chat, sem precisar abrir a aba "Evidências".
11. Como aluno, quero ver o score de relevância de cada fonte citada, para entender quão confiável é cada trecho usado na resposta.
12. Como aluno, quero que perguntas sem uso de RAG (`fontes_citadas` vazio) continuem renderizando normalmente, sem espaço vazio ou erro na UI.
13. Como mantenedor, quero uma função pura que extraia as fontes citadas a partir de `tool_calls`, para testá-la isoladamente sem chamar a LLM.
14. Como aluno, quero acessar uma aba "Progresso" que mostra minhas dificuldades ao longo do tempo, para identificar padrões nos meus pontos fracos.
15. Como aluno, quero ver minha taxa de acerto em revisões ativas (CORRECT/PARTIAL/INCORRECT), para saber se estou evoluindo.
16. Como aluno, quero ver os temas mais recorrentes nas minhas dificuldades e revisões malsucedidas, para priorizar o que estudar.
17. Como avaliador do trabalho, quero ver um painel de progresso de aprendizado, para ter evidência visual do critério "melhoria de aprendizado" do Trabalho 2.
18. Como mantenedor, quero que `/api/analytics/progresso` retorne dados agregados sem chamar a LLM, para que o painel carregue rápido e sem custo de tokens.
19. Como aluno, quero ver um estado vazio amigável na aba "Progresso" quando ainda não tenho dificuldades nem revisões registradas, para a tela não parecer quebrada no início do uso.
20. Como mantenedor, quero testes automatizados para `JsonCollectionStore`, para que mudanças futuras em `storage.py` não quebrem atomicidade ou validação sem aviso.
21. Como mantenedor, quero testes automatizados para `verificar_saude`, para confiar no diagnóstico do `/api/health` em diferentes cenários (RAG vazio, RAG indexado, LLM mock).
22. Como mantenedor, quero testes automatizados para o tratamento de PDF corrompido, para detectar regressões na ingestão de documentos.
23. Como mantenedor, quero testes automatizados para `extrair_fontes_citadas`, para que o formato de `fontes_citadas` não quebre o frontend silenciosamente.
24. Como mantenedor, quero testes automatizados para `LearningAnalytics` com dados de fixture, para validar a lógica de agregação sem depender da LLM remota.
25. Como mantenedor, quero que todos os módulos novos funcionem com `RAG_MODE=lexical` (sem sentence-transformers/FAISS), para manter o modo leve de deploy.

## Implementation Decisions

### 1. Storage reliability layer (`JsonCollectionStore`)

- Substitui as funções soltas `_read_json`/`_write_json` em `storage.py` por uma classe `JsonCollectionStore(path: Path)` com `ler() -> list[dict]` e `escrever(itens: list[dict]) -> None`.
- `escrever()` é atômico: serializa para um arquivo temporário no mesmo diretório e usa `os.replace()` para substituir o arquivo final — evita arquivos truncados em caso de falha no meio da escrita.
- Nenhuma dependência nova: lock baseado em criação exclusiva de arquivo (`open(..., "x")`) com retry curto, suficiente para o cenário de instância única do Hugging Face Spaces. Concorrência multi-processo real fica fora de escopo (ver "Out of Scope").
- `AgendaStore`, `TarefaStore`, `DificuldadeStore`, `RevisaoStore` passam a compor uma instância de `JsonCollectionStore` em vez de chamar funções de módulo diretamente.
- Validação adicionada nos pontos de escrita (não no `JsonCollectionStore`, que permanece agnóstico de schema):
  - `AgendaStore.adicionar` / `TarefaStore.adicionar`: campos de data (`data`, `prazo`) devem ser `AAAA-MM-DD` ou string vazia; valor inválido levanta `ValueError`.
  - `TarefaStore.adicionar`: `prioridade` deve estar em `{"baixa", "média", "alta"}`.
  - `web_api/main.py`: `ValueError` desses validadores é convertido em `HTTPException(422)` com a mensagem original (em vez de cair no handler genérico 500).

### 2. Health aggregator (`src/health.py`)

- Novo módulo com `verificar_saude(rag: RagEngine | None = None, verbose: bool = False) -> dict`.
- Sem chamada à LLM por padrão. Retorna:
  - `rag`: `{documentos, chunks, modo_recuperacao}` (reaproveita `RagEngine`/`_resumo_base`).
  - `llm`: `{modo, configurado}` — `configurado` é `True` se `settings.usando_mock` ou se `settings.validate_llm()` não levanta exceção (sem chamar a rede).
  - `storage`: `{ok: bool, erro: str | None}` — escreve, lê e remove um arquivo `_healthcheck.tmp` em `settings.storage_dir`.
  - `ok`: `True` somente se `rag`, `llm.configurado` e `storage.ok` forem todos saudáveis.
- Quando `verbose=True` (via `/api/health?verbose=true`), adiciona um campo `llm_ping` reaproveitando a lógica de `GemmaClient().ping()` já usada por `/api/debug/gemma-ping`.
- `web_api/main.py`: `/api/health` passa a chamar `verificar_saude()`, mantendo todos os campos hoje existentes (`ok`, `modo_llm`, `llm_provider`, etc.) e adicionando os novos campos de forma aditiva (sem quebrar consumidores atuais).

### 3. RAG ingestion error handling

- `ler_arquivo` (em `src/rag.py`) passa a capturar exceções genéricas ao processar PDFs (`PdfReader`/extração de página) e retornar string vazia em caso de falha, sem propagar a exceção.
- `carregar_documentos` coleta as falhas em uma lista `documentos_com_erro: list[dict]` (formato `{"arquivo": <caminho relativo>, "erro": <mensagem>}`), retornada junto com os documentos válidos.
- `RagEngine.reindexar` armazena essa lista em `self.documentos_com_erro` e a inclui no dicionário de retorno.
- `web_api/main.py` (`_resumo_base`): inclui `documentos_com_erro` no resumo, exposto em `/api/status`.

### 4. Citation extraction (`extrair_fontes_citadas`)

- Nova função pura `extrair_fontes_citadas(resultados: list[dict]) -> list[dict]`, em `src/agent.py` (próxima ao `_responder_final`, mesmo padrão de funções utilitárias já presente no módulo).
- Percorre `resultados` (a lista `tool_calls`), procura `documentos_recuperados` e `materiais_relevantes` em cada `saida`, e retorna uma lista deduplicada (por `id`, fallback `fonte+score`) de `{"fonte": str, "id": str, "score": float}`, ordenada por `score` decrescente.
- `JarvisAgent.responder()` passa a incluir `"fontes_citadas": extrair_fontes_citadas(resultados)` no dicionário retornado, ao lado de `resposta` e `tool_calls`. Lista vazia quando não há fontes (ex.: conversa casual, fallback acadêmico sem RAG).
- `web_api/main.py` (`/api/chat`): repassa `fontes_citadas` sem alteração — o endpoint já retorna o dicionário do agente diretamente.

### 5. Learning analytics (`src/analytics.py`)

- Novo módulo com a classe `LearningAnalytics`, construída com `DificuldadeStore` e `RevisaoStore` (instanciados por padrão se não fornecidos — mesmo padrão de `LearningService`).
- Método `resumo(dias: int = 30) -> dict` retorna:
  - `dificuldades_por_topico`: lista de `{topico, quantidade}`, ordenada por quantidade decrescente.
  - `dificuldades_por_periodo`: lista de `{data: "AAAA-MM-DD", quantidade}` para os últimos `dias` dias (a partir de `criado_em` das dificuldades).
  - `revisoes`: `{total, avaliadas, taxa_acerto, distribuicao: {CORRECT, PARTIAL, INCORRECT}, nota_media}` — `taxa_acerto` é `CORRECT / avaliadas` (0 se `avaliadas == 0`).
  - `temas_recorrentes`: lista combinada de tópicos de dificuldades e de revisões avaliadas como `PARTIAL`/`INCORRECT`, ordenada por frequência.
- Não chama a LLM nem o RAG — opera apenas sobre os dados já persistidos em `storage/`.

### 6. Endpoint e frontend

- Novo endpoint `GET /api/analytics/progresso?dias=30` em `web_api/main.py`, chama `LearningAnalytics().resumo(dias=dias)`.
- Frontend (`frontend/src/App.jsx`):
  - `navigationItems` ganha uma nova entrada `{ id: 'progresso', label: 'Progresso', icon: TrendingUp }` (ícone já disponível via `lucide-react`).
  - Novo componente `ProgressoView`, busca `/api/analytics/progresso` ao ser ativado, segue o padrão de `MaterialsView`/`AgendaView` (`section.workspace-view`, `view-header`).
  - Visualizações em barras CSS reaproveitando classes existentes (`.evidence-pill`, `.list-card`), sem novas dependências de gráficos.
  - Estado vazio (`total dificuldades == 0 && total revisoes == 0`) segue o padrão de mensagens "Nenhum/Nenhuma ..." já usado em `TasksView`/`AgendaView`.
  - `MessageBubble` passa a renderizar `message.fontes_citadas` (vindo de `/api/chat`) como uma linha de chips abaixo do conteúdo markdown, reaproveitando o estilo `.source-chip` e o `formatScore` já usados em `ContextPanel`/`extractSources`. Quando `fontes_citadas` é vazio ou ausente, nada é renderizado (sem espaço extra).

## Testing Decisions

Bom teste aqui significa testar **comportamento observável** (entrada → saída de cada módulo novo), não detalhes de implementação como o mecanismo exato de lock de arquivo ou a ordem interna de iteração.

Módulos com testes nesta PRD:

- **`JsonCollectionStore` (módulo 1)**: escreve uma lista, lê de volta e confirma round-trip; confirma que uma escrita seguida de leitura não deixa arquivo temporário para trás; testa validação de data/prioridade em `AgendaStore.adicionar`/`TarefaStore.adicionar` (entrada inválida levanta `ValueError`).
- **`verificar_saude` (módulo 2)**: roda com `RAG_MODE=lexical` e `LLM_MODE=mock` e confirma que `ok=True` e que as chaves `rag`, `llm`, `storage` têm o formato esperado; simula RAG vazio (sem documentos) e confirma que `rag.modo_recuperacao` reflete isso sem que `ok` necessariamente vire `False` (RAG vazio é um estado válido, não uma falha de saúde).
- **RAG ingestion + citations (módulos 3 e 4)**: `carregar_documentos` com um PDF corrompido (fixture com bytes inválidos) não levanta exceção e popula `documentos_com_erro`; demais documentos válidos continuam sendo carregados. `extrair_fontes_citadas` testado com: lista vazia, um único `tool_call` de RAG, múltiplos `tool_calls` com fontes duplicadas (confirma deduplicação e ordenação por score).
- **`LearningAnalytics` (módulo 5)**: com dados de fixture (`Dificuldade`/`Revisao` criados diretamente, sem passar por LLM), confirma `taxa_acerto`, `dificuldades_por_topico` e `temas_recorrentes` para cenários com 0, 1 e múltiplos registros, incluindo o caso `avaliadas == 0` (sem divisão por zero).

Prior art no projeto (seguir o mesmo estilo leve de `pytest`, sem mocks pesados):

- `tests/test_storage.py` — padrão de criar dataclass e verificar campos auto-gerados.
- `tests/test_chunking.py` — fixtures de `RagEngine`/documentos para RAG.
- `tests/test_learning_features.py` — construção direta de `Dificuldade`/`Revisao`.
- `tests/test_llm_config.py` — manipulação de `LLM_MODE`/variáveis de ambiente para testar comportamento de `mock`.

Frontend (módulo 6) e o módulo 7 (suíte de testes do agente/endpoints) não recebem testes automatizados nesta PRD — ver "Out of Scope".

## Out of Scope

- **Módulo 7 — suíte de testes do `JarvisAgent` (loop de tool calling) e dos 25+ endpoints de `web_api/main.py` via `TestClient`**: continua sendo a maior lacuna identificada na revisão de estado, mas fica para uma PRD futura.
- **Testes automatizados de frontend**: o projeto não tem infraestrutura de Jest/Vitest; as mudanças do módulo 6 (chips de citação, aba "Progresso") serão verificadas manualmente.
- **Modularização de `App.jsx`** (986 linhas em um único arquivo): refatoração separada, não tratada aqui.
- **Lock de arquivo multi-processo real / migração para banco de dados**: fora de escopo — o projeto roda como instância única no Hugging Face Spaces; a escrita atômica resolve o caso de corrupção por interrupção, não concorrência multi-processo.
- **Autenticação, multiusuário, banco de dados remoto**: já fora de escopo no PRD original do projeto.
- **Streaming de respostas do chat**.

## Further Notes

- Os nomes legados `LLM_MODE=gemma` e `GEMMA_*` continuam sendo a interface pública de configuração; `verificar_saude` deve usar `settings.gemma_*`/`settings.usando_mock` como hoje, sem introduzir novos nomes de variáveis de ambiente.
- Todos os módulos novos devem funcionar com `RAG_MODE=lexical` (sem `sentence-transformers`/`faiss`), preservando o modo leve de deploy documentado em `src/rag.py`.
- `/api/health` deve permanecer compatível com consumidores atuais — campos novos são aditivos, nenhum campo existente é removido ou renomeado.
- Esta PRD cobre 6 dos 7 módulos identificados na revisão de estado do projeto; o módulo 7 (testes de agente/endpoints) permanece registrado como próximo passo natural após esta entrega.
