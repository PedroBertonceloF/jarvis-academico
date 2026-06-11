# Auditoria visual — JARVIS Acadêmico

## Diagnóstico

O JARVIS já possuía uma estrutura funcional adequada para a entrega: navegação lateral, chat principal, upload de materiais, tarefas, agenda, fontes, logs e painel de evidências. A revisão visual anterior resolveu parte da hierarquia, mas ainda deixava a identidade apoiada na paleta antiga e em um símbolo desenhado dentro do `App.jsx`.

Essa versão sincroniza o produto com o branding aprovado no pacote `jarvis_branding_complete(1).zip` e evolui a paleta para temas claro/escuro acessíveis.

## Branding aprovado

- Conceito: **F01 / C01 — Convergência orbital**.
- Símbolo: três trajetórias orbitais, múltiplas fontes, síntese, decisão e aprendizagem contínua.
- Direção cromática: Charcoal Black no escuro, Porcelain Lavender no claro, violeta `#8A83DA` no escuro e Deep Mauve no claro como identidade.
- Aplicação: tema escuro padrão, tema claro opcional e escolha persistida em `localStorage`.

## Ajustes aplicados

| Área | Implementação |
|---|---|
| Marca | O SVG oficial é usado como máscara CSS e muda de cor por tema via `--brand`. |
| Sidebar | Item ativo em `--brand-soft`, linha ativa em `--brand` e contraste adequado nos dois temas. |
| Header | Status da LLM, label “Espaço de estudo” e alternador de tema usam presença violeta controlada. |
| Chat | Contexto fixo corrigido para Disciplina — Inteligência Artificial; mensagem do usuário adapta fundo e borda por tema. |
| Composer | Foco e envio usam marca do tema atual, sem gradiente e sem neon. |
| Inspector | Cards e superfícies usam tokens para leitura em claro e escuro. |
| Materiais | Upload e ações principais usam marca; sucesso/erro preservados como semântica. |
| Tarefas | Ação principal usa marca, concluir em verde e erro/alerta nas cores semânticas. |
| Agenda | Marcadores usam marca do tema, sem verde decorativo. |
| Evidências | RAG e recuperação usam marca; fallback em dourado; erros em vermelho; sucesso real em verde. |

## Paleta vigente

### Tema escuro

- Fundo: `#2B2B2B`.
- Superfícies: `#353238`, `#3E3942`, `#48414E`.
- Texto principal: `#F7F3F7`.
- Texto de apoio: `#D3CCD5`.
- Texto secundário: `#A49CA6`.
- Marca principal: `#8A83DA`.
- Marca forte: `#B4AAEB`.
- Profundidade: `#5D536B`.

### Tema claro

- Fundo: `#F4F1F5`.
- Superfícies: `#FCFAFD`, `#E7E1E9`, `#DDD6E0`.
- Texto principal: `#2B2B2B`.
- Texto de apoio e marca: `#5D536B`.
- Texto secundário: `#716978`.
- Profundidade: `#A49CA6`.
- Violeta secundário: `#7567B3`.

## Referências antigas removidas

- Teal deixou de ser identidade visual.
- Verde deixou de ser usado como destaque genérico.
- O símbolo inline antigo foi removido do React.
- O fundo perdeu o padrão pontilhado que poderia parecer partículas.
- O fundo OLED quase absoluto foi substituído por Charcoal Black.
- A área fixa do chat deixou de apresentar o sistema como preparação para uma prova específica.

## Riscos de regressão monitorados

- Chat longo precisa manter rolagem interna no fim da conversa.
- Textos longos de fontes/logs não podem causar overflow horizontal.
- Avatar e favicon precisam renderizar a partir dos assets oficiais.
- Mobile não pode comprimir o chat por causa do inspector.
- Estados de sucesso, alerta e erro continuam sem depender apenas de cor.
- O tema claro não pode parecer clínico ou branco puro.
- O alternador de tema precisa persistir após reload.

## Checklist de validação

- [x] ZIP inspecionado antes da extração.
- [x] ZIP extraído fora do repositório.
- [x] Apenas assets de produção copiados para o Git.
- [x] SVG oficial usado como base da marca.
- [x] Favicons e PNGs gerados a partir dos SVGs violeta/creme.
- [x] React usa componente dedicado de marca.
- [x] Paleta anterior removida do frontend.
- [x] Temas claro/escuro implementados com tokens.
- [x] Tema escuro preservado como padrão.
- [x] Escolha de tema persistida em `localStorage`.
- [x] Contexto fixo corrigido para Disciplina — Inteligência Artificial.
- [x] Design system documentado.
