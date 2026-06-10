# Auditoria visual — JARVIS Acadêmico

## Diagnóstico

O JARVIS já possuía uma estrutura funcional adequada para a entrega: navegação lateral, chat principal, upload de materiais, tarefas, agenda, fontes, logs e painel de evidências. A revisão visual anterior resolveu parte da hierarquia, mas ainda deixava a identidade apoiada na paleta antiga e em um símbolo desenhado dentro do `App.jsx`.

Essa versão sincroniza o produto com o branding aprovado no pacote `jarvis_branding_complete(1).zip`.

## Branding aprovado

- Conceito: **F01 / C01 — Convergência orbital**.
- Símbolo: três trajetórias orbitais, múltiplas fontes, síntese, decisão e aprendizagem contínua.
- Direção cromática: **80% editorial escuro + 20% energia violeta cósmica**.
- Aplicação: dark-only, sem alternador de tema e sem preferência automática para tema claro.

## Ajustes aplicados

| Área | Implementação |
|---|---|
| Marca | O SVG improvisado foi removido e substituído por assets oficiais em `frontend/public/brand/`. |
| Sidebar | Símbolo lavanda, item ativo em `--brand-soft` e linha ativa em `--brand`. |
| Header | Eyebrow e status remoto em lavanda; chunks permanecem neutros. |
| Chat | Avatar oficial do assistente, mensagem do usuário em violeta profundo e resposta neutra. |
| Composer | Foco e envio em lavanda, sem gradiente e sem neon. |
| Inspector | Labels, fontes, métricas e logs com detalhes lavanda e texto técnico em mono. |
| Materiais | Upload e ações principais em lavanda; sucesso/erro preservados como semântica. |
| Tarefas | Ação principal lavanda, concluído em verde e erro/alerta nas cores semânticas. |
| Agenda | Marcadores em lavanda, sem verde decorativo. |
| Evidências | RAG e métricas em lavanda; fallback em dourado; erros em vermelho; sucesso em verde. |

## Paleta vigente

- Fundo: `#050505`.
- Superfícies: `#14121D`, `#1D1928`, `#262335`.
- Texto principal: `#FBF5F0`.
- Texto de apoio: `#C7C2CE`.
- Texto secundário: `#8E8999`.
- Marca principal: `#8A83DA`.
- Marca profunda: `#463699`.
- Energia ambiental: `#3A0CA3`.
- Sucesso: `#80B89A`.
- Aviso: `#D4A85F`.
- Erro: `#D97972`.

## Referências antigas removidas

- Teal deixou de ser identidade visual.
- Verde deixou de ser usado como destaque genérico.
- O símbolo inline antigo foi removido do React.
- O fundo perdeu o padrão pontilhado que poderia parecer partículas.
- O halo ambiental foi reduzido a uma única energia violeta controlada.

## Riscos de regressão monitorados

- Chat longo precisa manter rolagem interna no fim da conversa.
- Textos longos de fontes/logs não podem causar overflow horizontal.
- Avatar e favicon precisam renderizar a partir dos assets oficiais.
- Mobile não pode comprimir o chat por causa do inspector.
- Estados de sucesso, alerta e erro continuam sem depender apenas de cor.

## Checklist de validação

- [x] ZIP inspecionado antes da extração.
- [x] ZIP extraído fora do repositório.
- [x] Apenas assets de produção copiados para o Git.
- [x] SVG oficial usado como base da marca.
- [x] Favicons e PNGs gerados a partir dos SVGs violeta/creme.
- [x] React usa componente dedicado de marca.
- [x] Paleta anterior removida do frontend.
- [x] Design system documentado.
- [x] Dark-only preservado.
