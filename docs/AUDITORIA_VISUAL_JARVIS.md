# Auditoria visual — JARVIS Acadêmico

## Diagnóstico atual

O JARVIS já possui uma estrutura funcional adequada para a entrega: navegação lateral, chat principal, upload de materiais, tarefas, agenda, fontes, logs e painel de evidências. O problema principal não está na arquitetura da interface, mas na linguagem visual.

Pontos que enfraquecem a percepção de produto autoral:

- excesso de ciano/roxo neon;
- múltiplos halos no fundo;
- sombras grandes em superfícies permanentes;
- cards aninhados em quase todas as áreas;
- raios muito altos e repetidos;
- símbolo `BrandOrb` com aparência genérica de IA;
- textos em inglês em uma aplicação acadêmica em português;
- painel contextual com peso visual similar ao chat;
- evidências técnicas com boa informação, mas ainda com aparência de card-stack.

## Referências analisadas

### AquaIA

Arquivos analisados:

- `/home/matteo/Faculdade/aquaia_ufms/static/src/input.css`;
- `/home/matteo/Faculdade/aquaia_ufms/templates/base.html`;
- `/home/matteo/Faculdade/aquaia_ufms/templates/index.html`;
- assets em `/home/matteo/Faculdade/aquaia_ufms/static/assets/brand/`.

Princípios aproveitáveis:

- hierarquia editorial forte;
- labels pequenas e objetivas;
- métricas com números grandes;
- bordas finas e espaços generosos;
- teal como identidade controlada;
- seções separadas por ritmo, não apenas por cards.

Elementos que não devem ser copiados:

- assets de ondas;
- wordmark;
- paleta clara integral;
- navegação e estrutura de telas específicas do AquaIA.

### Portfólio

Arquivos analisados:

- `/home/matteo/ProjetosPessoais/MeuSite/index.html`;
- `/home/matteo/ProjetosPessoais/MeuSite/style.css`;
- `/home/matteo/ProjetosPessoais/MeuSite/script.js`;
- assets em `/home/matteo/ProjetosPessoais/MeuSite/assets/`.

Princípios aproveitáveis:

- estética editorial autoral;
- grid e textura discretos;
- `Space Grotesk` para display;
- `IBM Plex Mono` para detalhes técnicos;
- transições curtas;
- hover com deslocamento pequeno;
- cards usados com parcimônia.

Elementos que não devem ser copiados:

- logo `teo`;
- textura/frame;
- command palette;
- estrutura de portfólio/landing page.

## Direção visual

Conceito: **JARVIS Study OS — editorial academic workspace**.

A interface deve manter o produto operacional, mas trocar a linguagem neon por uma versão escura editorial: fundo quase preto, grade sutil, teal controlado, tipografia com mais personalidade, linhas finas e menos profundidade permanente.

## Mapa de componentes

| Área | Mudança planejada |
|---|---|
| Marca | Substituir orb CSS por monograma/grafo em SVG inline. |
| Sidebar | Reduzir peso, usar borda lateral e navegação por linha. |
| Header | Trocar card por cabeçalho editorial com status compacto. |
| Sessão do chat | Remover gradiente e transformar em cabeçalho operacional. |
| Quick prompts | Reduzir para sugestões editoriais menores e responsivas. |
| Mensagens | Respostas mais planas; user bubble compacta; metadados em mono. |
| Composer | Manter sticky/elevado, mas com borda e raio menores. |
| Inspector | Separar seções por linhas, priorizando fontes e ferramentas. |
| Materiais | Upload e lista com visual mais editorial. |
| Tarefas | Lista operacional com linhas, não card pesado por item. |
| Agenda | Timeline mais limpa e legível. |
| Evidências | Auditoria acadêmica com métricas, timeline e JSON expansível. |

## Riscos de regressão

- Quebra de responsividade em mobile por causa do grid principal.
- Textos longos de fontes/logs causando overflow.
- Botões de ícone sem label acessível.
- Build do Vite falhar por import ou JSX inválido.
- Alteração visual acidental em elementos que indicam fallback/RAG/tool calling.

## Checklist de implementação

- [x] Ler `frontend/src/App.jsx`.
- [x] Ler `frontend/src/styles.css`.
- [x] Localizar repositórios de referência.
- [x] Confirmar `git status` dos três projetos.
- [x] Usar AquaIA e portfólio apenas como leitura.
- [x] Atualizar tokens visuais.
- [x] Substituir marca genérica.
- [x] Ajustar textos e labels em português.
- [x] Reduzir cards, sombras e halos.
- [x] Melhorar chat, inspector e evidências.
- [x] Revisar responsividade por CSS e breakpoints.
- [x] Rodar build e testes automatizados disponíveis.

## Validação visual

O app integrado foi iniciado localmente em `http://127.0.0.1:7860` e o endpoint `/api/status` respondeu corretamente. A verificação visual automatizada por screenshot não pôde ser executada porque este ambiente não possui `agent-browser`, Playwright ou Chromium instalados no PATH.
