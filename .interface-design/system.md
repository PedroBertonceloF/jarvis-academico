# Sistema de interface — JARVIS Acadêmico

## Intent

Usuário: aluno de Computação estudando IA e avaliador técnico do projeto.

Tarefa principal: estudar com suporte de IA, consultar fontes, organizar tarefas e verificar evidências de RAG/tool calling.

Sensação desejada: acadêmico, técnico, organizado, premium, cósmico e rastreável.

## Domain

Estudos, fontes, RAG, revisão ativa, evidências, chunks, scores, tool calling, tarefas, agenda, dificuldades, fallback.

## Color World

- Charcoal Black `#2B2B2B` como base do tema escuro padrão.
- Porcelain Lavender `#F4F1F5` como base do tema claro opcional.
- Violeta `#8A83DA` para identidade, RAG, foco ativo, avatar, links e botões principais no escuro.
- Deep Mauve `#5D536B` para identidade, RAG, foco ativo, avatar, links e botões principais no claro.
- Ash Lavender `#A49CA6` para metadados, texto secundário e apoio no escuro, não como marca principal.
- Superfícies grafite-malva e branco-lavanda para separar áreas de trabalho sem branco puro.
- Amarelo/dourado para alertas e atenção acadêmica.
- Verde somente para sucesso, concluído ou online.

## Signature

Símbolo orbital oficial e painel de evidências/fonte/RAG sempre próximos da conversa. A interface deve deixar claro quando a resposta veio de fonte recuperada, ferramenta interna ou fallback.

## Defaults a rejeitar

- Chat genérico sem fontes; preferir evidências visíveis.
- Dashboard acadêmico estático; preferir workspace de estudo com ações.
- IA apresentada como autoridade absoluta; preferir transparência, fallback e limites.

## Tokens e padrões atuais

- Tema: dark por padrão, light opcional persistido em `localStorage` com a chave `jarvis-theme`.
- Superfícies: `--surface`, `--surface-strong`, `--surface-soft`.
- Bordas: `--border` e `--border-strong`.
- Texto: `--text`, `--text-muted`, `--text-soft`.
- Acentos: `--brand`, `--brand-deep`, `--warning`, `--success`, `--danger`, `--info`.
- Presença cromática: cerca de 10% de violeta visível, concentrado em logo, item ativo, labels, RAG, foco e ações principais.
- Raios: `--radius-xl`, `--radius-lg`, `--radius-md`.
- Profundidade: sombras amplas em contêineres principais e surface shifts em componentes internos.

## Estados interativos

- Navegação lateral deve indicar item ativo.
- Respostas devem exibir modo: RAG fundamentado, tool calling, fallback ou resposta direta.
- Upload, envio e atualização precisam de estado de carregamento.
- Logs e fontes precisam preservar legibilidade mesmo com dados técnicos longos.

## Acessibilidade e responsividade

- Manter contraste adequado no tema escuro e no tema claro.
- Garantir foco visível em botões, inputs e navegação.
- Evitar que painéis de evidência comprimam o chat no mobile.
- Labels e títulos devem explicar ações técnicas sem depender só de cor.

## Limites

Não alterar integração Gemma/LIA, dataset ou critérios de avaliação sem motivo acadêmico claro. A interface deve continuar priorizando estudo, fontes e evidências.
