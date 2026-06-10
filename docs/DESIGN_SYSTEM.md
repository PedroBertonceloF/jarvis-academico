# Design system — JARVIS Acadêmico

## Intent

Usuário principal: aluno de Computação estudando IA e avaliador técnico do trabalho.

Tarefa principal: consultar materiais, conversar com o assistente, organizar estudos e auditar evidências de RAG/tool calling.

Sensação desejada: acadêmico, técnico, autoral, silencioso, confiável e rastreável.

## Princípios

- A conversa é o centro da experiência.
- Evidências, fontes e ferramentas devem estar sempre próximas da resposta.
- A interface deve parecer produto acadêmico, não dashboard gamer ou template de IA.
- Estados técnicos devem ser legíveis sem depender só de cor.
- Cards são reservados para unidades independentes; listas e linhas resolvem conteúdo secundário.

## Tokens conceituais

### Cores

- Fundo: preto editorial com grade discreta.
- Superfícies: carvão e grafite, sem glassmorphism pesado.
- Texto: papel quente para títulos e corpo.
- Acento principal: teal.
- Acento secundário: azul frio discreto.
- Semânticas: dourado para aviso, verde para sucesso, vermelho seco para erro.

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

## Assinatura visual

A assinatura do JARVIS é o **Inspector acadêmico**: fontes, ferramentas, tarefas, agenda e logs perto da conversa, com uma textura sutil de grafo/chunks no fundo e metadados em mono.

## Padrões de acessibilidade

- Foco visível em botões, inputs e navegação.
- Alvos de toque mínimos de 44px em mobile.
- Botões de ícone com `title` ou `aria-label`.
- Contraste alto no tema escuro.
- Sem informação transmitida apenas por cor.
