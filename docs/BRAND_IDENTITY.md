# Identidade de marca — JARVIS Acadêmico

## Símbolo aprovado

A marca aprovada para o JARVIS Acadêmico é **F01 / C01 — Convergência orbital**.

O símbolo representa:

- três trajetórias orbitais;
- múltiplas fontes de conhecimento;
- síntese de informação;
- decisão assistida;
- aprendizagem contínua;
- organização acadêmica;
- núcleo de conhecimento.

## Origem dos assets

Os assets foram gerados a partir do pacote local:

```text
/home/matteo/Downloads/jarvis_branding_complete(1).zip
```

O ZIP foi extraído fora do repositório em:

```text
/home/matteo/.cache/jarvis-branding-source/
```

O arquivo base utilizado foi:

```text
jarvis_branding/04_master/svg/jarvis_symbol_master.svg
```

O micro símbolo utilizado para favicon veio de:

```text
jarvis_branding/04_master/svg/jarvis_symbol_micro.svg
```

## Direção visual

A interface possui dois temas:

- escuro padrão em **Charcoal Black**;
- claro opcional em **Porcelain Lavender**.

A escolha do usuário é persistida em `localStorage` pela chave `jarvis-theme`. No primeiro acesso, o tema escuro é usado.

Características:

- acadêmica;
- técnica;
- premium;
- cósmica sem neon excessivo;
- editorial;
- rastreável;
- sem aparência gamer;
- sem aparência cripto;
- sem visual genérico de IA.

## Paleta

| Papel | Tema escuro | Tema claro |
|---|---|---|
| Fundo principal | `#2B2B2B` | `#F4F1F5` |
| Fundo suave | `#302E32` | `#ECE7EE` |
| Superfície | `#353238` | `#FCFAFD` |
| Superfície forte | `#3E3942` | `#E7E1E9` |
| Superfície suave | `#48414E` | `#DDD6E0` |
| Texto principal | `#F7F3F7` | `#2B2B2B` |
| Texto de apoio | `#D3CCD5` | `#5D536B` |
| Texto secundário | `#A49CA6` | `#716978` |
| Marca principal | `#8A83DA` | `#5D536B` |
| Marca forte | `#B4AAEB` | `#463699` |
| Violeta secundário | `#7567B3` | `#7567B3` |
| Profundidade | `#5D536B` | `#A49CA6` |
| Sucesso | `#80B89A` | `#4F765F` |
| Aviso | `#D4A85F` | `#8A6426` |
| Erro | `#D97972` | `#A34F4A` |

## Regras de cor

- Use `#8A83DA` para logo, avatar, foco, links, item ativo, RAG e ações principais no tema escuro.
- Use Deep Mauve para logo, avatar, foco, links, item ativo, RAG e ações principais no tema claro.
- Use Ash Lavender `#A49CA6` como apoio, metadado e profundidade discreta, não como marca principal.
- Use Porcelain Lavender como fundo claro principal, nunca branco puro.
- Use `#80B89A` / `#4F765F` somente para sucesso, concluído ou online.
- Não use verde para marca, RAG, links, botões primários ou navegação ativa.
- Não use Deep Mauve como texto pequeno no tema escuro.
- Não use Ash Lavender como texto pequeno sobre Porcelain sem contraste suficiente.
- Não aplicar violeta em todas as superfícies; a identidade deve aparecer em pontos estratégicos.

## Tema e marca

O componente `BrandMark` não troca imagens por tema. Ele usa o SVG oficial `jarvis-symbol.svg` como máscara CSS e preenche o símbolo com `--brand`.

- Escuro: símbolo em violeta `#8A83DA`.
- Claro: símbolo em Deep Mauve.
- Favicons e app icons continuam usando os assets estáticos gerados a partir do pacote de branding.

## Assets de produção

Arquivos versionados:

```text
frontend/public/brand/jarvis-symbol.svg
frontend/public/brand/jarvis-symbol-lavender.svg
frontend/public/brand/jarvis-symbol-paper.svg
frontend/public/brand/jarvis-symbol-micro.svg
frontend/public/brand/jarvis-symbol-outline.svg
frontend/public/brand/jarvis-avatar-64.png
frontend/public/brand/jarvis-avatar-128.png
frontend/public/brand/jarvis-app-icon-192.png
frontend/public/brand/jarvis-app-icon-512.png
frontend/public/brand/favicon.svg
frontend/public/brand/favicon.ico
frontend/public/brand/favicon-16.png
frontend/public/brand/favicon-32.png
frontend/public/brand/favicon-48.png
frontend/public/brand/social-preview.svg
```

## Tamanhos recomendados

| Uso | Asset |
|---|---|
| Sidebar expandida | `BrandMark` com máscara CSS, 38 px ou mais |
| Sidebar recolhida | `BrandMark` com máscara CSS, 38 px |
| Avatar do assistente | `BrandMark` com máscara CSS, 30 a 40 px |
| Favicon | `jarvis-symbol-micro.svg` ou `favicon-*` |
| App icon | `jarvis-app-icon-192.png` e `jarvis-app-icon-512.png` |
| Social preview | `social-preview.svg` |

## Usos proibidos

- Não redesenhar o símbolo manualmente em JSX.
- Não aplicar gradiente dentro do símbolo.
- Não usar símbolo preto sobre fundo escuro.
- Não usar PNG antigo do aplicativo.
- Não adicionar o ZIP completo ao repositório.
- Não voltar ao tema escuro exclusivo.
- Não usar branco puro como fundo principal do tema claro.
- Não usar glow pulsante, partículas, estrelas ou aurora pesada.
- Não usar a marca como decoração repetida.
