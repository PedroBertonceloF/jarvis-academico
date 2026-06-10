# Sistema de interface — JARVIS Acadêmico

## Intent

Usuário: aluno de Computação estudando IA e avaliador técnico do projeto.

Tarefa principal: estudar com suporte de IA, consultar fontes, organizar tarefas e verificar evidências de RAG/tool calling.

Sensação desejada: acadêmico, técnico, organizado e rastreável.

## Domain

Estudos, fontes, RAG, revisão ativa, evidências, chunks, scores, tool calling, tarefas, agenda, dificuldades, fallback.

## Color World

- Fundo escuro técnico para foco prolongado.
- Superfícies escuras levemente elevadas para separar áreas de trabalho.
- Ciano para evidência, RAG e foco ativo.
- Violeta como acento de IA.
- Amarelo/dourado para alertas e atenção acadêmica.
- Verde para sucesso e estados fundamentados.

## Signature

Painel de evidências/fonte/RAG sempre próximo da conversa. A interface deve deixar claro quando a resposta veio de fonte recuperada, ferramenta interna ou fallback.

## Defaults a rejeitar

- Chat genérico sem fontes; preferir evidências visíveis.
- Dashboard acadêmico estático; preferir workspace de estudo com ações.
- IA apresentada como autoridade absoluta; preferir transparência, fallback e limites.

## Tokens e padrões atuais

- Tema: dark workspace.
- Superfícies: `--surface`, `--surface-strong`, `--surface-soft`.
- Bordas: `--border` e `--border-strong`.
- Texto: `--text`, `--text-muted`, `--text-soft`.
- Acentos: `--cyan`, `--violet`, `--gold`, `--green`, `--red`.
- Raios: `--radius-xl`, `--radius-lg`, `--radius-md`.
- Profundidade: sombras amplas em contêineres principais e surface shifts em componentes internos.

## Estados interativos

- Navegação lateral deve indicar item ativo.
- Respostas devem exibir modo: RAG fundamentado, tool calling, fallback ou resposta direta.
- Upload, envio e atualização precisam de estado de carregamento.
- Logs e fontes precisam preservar legibilidade mesmo com dados técnicos longos.

## Acessibilidade e responsividade

- Manter contraste alto no tema escuro.
- Garantir foco visível em botões, inputs e navegação.
- Evitar que painéis de evidência comprimam o chat no mobile.
- Labels e títulos devem explicar ações técnicas sem depender só de cor.

## Limites

Não alterar integração Gemma/LIA, dataset ou critérios de avaliação sem motivo acadêmico claro. A interface deve continuar priorizando estudo, fontes e evidências.
