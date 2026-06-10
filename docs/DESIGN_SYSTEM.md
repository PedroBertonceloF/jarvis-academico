# Design system — JARVIS Acadêmico

## Intent

Usuário principal: aluno de Computação estudando IA e avaliador técnico do trabalho.

Tarefa principal: consultar materiais, conversar com o assistente, organizar estudos e auditar evidências de RAG/tool calling.

Sensação desejada: acadêmico, técnico, autoral, silencioso, premium, cósmico e rastreável.

## Princípios

- A conversa é o centro da experiência.
- Evidências, fontes e ferramentas devem estar sempre próximas da resposta.
- A interface deve parecer produto acadêmico, não dashboard gamer, cripto ou template genérico de IA.
- Estados técnicos devem ser legíveis sem depender só de cor.
- Cards são reservados para unidades independentes; listas e linhas resolvem conteúdo secundário.

## Tokens conceituais

### Cores

- Fundo: `#050505`, preto editorial com grade discreta.
- Superfícies: `#14121D`, `#1D1928` e `#262335`, sem glassmorphism pesado.
- Texto: `#FBF5F0` para títulos e corpo, `#C7C2CE` para apoio e `#8E8999` para metadados.
- Acento principal: lavanda `#8A83DA`.
- Acento profundo: violeta `#463699` para seleção, chips e mensagem do usuário.
- Energia ambiental: violeta elétrico `#3A0CA3`, apenas em halo discreto e preview social.
- Semânticas: dourado para aviso, verde somente para sucesso/concluído/online, vermelho seco para erro.

O verde não é identidade visual. RAG, foco, links, avatar, item ativo e botão primário usam lavanda.

### Tipografia

- Display: `Space Grotesk`, com fallback para `Sora` e sans-serif.
- Corpo: `Inter`, com fallback de sistema.
- Técnico: `IBM Plex Mono`, com fallback monospace.

Uso:

- Display em títulos e números.
- Corpo em mensagens, descrições e formulários.
- Mono em labels técnicas, scores, timestamps, modelos, nomes de arquivo e JSON.

### Raios

- `--radius-xl`: superfícies principais.
- `--radius-lg`: painéis e cards independentes.
- `--radius-md`: listas, inputs e elementos técnicos.
- `--radius-pill`: badges e chips.

### Profundidade

Sombras devem aparecer em elementos elevados de verdade: composer, menu mobile, hover e painéis flutuantes. Superfícies fixas usam borda e contraste, não sombra permanente.

### Motion

- Transições entre 150ms e 240ms.
- Hover com deslocamento de 1px a 3px.
- Sem glow pulsante.
- Respeitar `prefers-reduced-motion`.

## Marca

O símbolo aprovado é **F01 / C01 — Convergência orbital**. Ele representa três trajetórias orbitais, múltiplas fontes, síntese, decisão e aprendizagem contínua.

Uso:

- `frontend/public/brand/jarvis-symbol-lavender.svg` para sidebar e avatar.
- `frontend/public/brand/jarvis-symbol-paper.svg` sobre fundos escuros quando o contraste exigir creme.
- `frontend/public/brand/jarvis-symbol-micro.svg` para favicon e tamanhos pequenos.
- Não redesenhar o símbolo manualmente no React.
- Não aplicar gradiente, neon ou sombra pulsante dentro do símbolo.

## Assinatura visual

A assinatura do JARVIS é o **Inspector acadêmico**: fontes, ferramentas, tarefas, agenda e logs perto da conversa, com metadados em mono e detalhes lavanda que conectam RAG, tool calling e evidências.

## Padrões de acessibilidade

- Foco visível em botões, inputs e navegação.
- Alvos de toque mínimos de 44px em mobile.
- Botões de ícone com `title` ou `aria-label`.
- Contraste alto no tema escuro.
- Sem informação transmitida apenas por cor.
