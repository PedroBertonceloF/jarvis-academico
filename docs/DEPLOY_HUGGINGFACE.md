# Deploy no Hugging Face Spaces

Este documento registra o processo seguro de deploy do JARVIS Academico no Hugging Face Spaces.

## Contexto

O repositorio GitHub (`origin/main`) e o repositorio do Hugging Face (`hf/main`) podem ter historicos diferentes.

Isso e intencional no fluxo atual: o GitHub preserva a linha principal de desenvolvimento, enquanto o Hugging Face recebe uma linha limpa de deploy criada a partir do estado atual do Space.

## Causa do bloqueio anterior

Um push direto de `main` para `hf/main` foi rejeitado porque o historico do GitHub continha o arquivo binario antigo:

```text
frontend/public/brand/social-preview-1200x630.png
```

Esse PNG foi substituido por:

```text
frontend/public/brand/social-preview.svg
```

Mesmo removido do estado atual, o blob binario ainda existia em commits antigos da `main`. Ao tentar enviar todo o historico para o Hugging Face, esse blob tambem era enviado e bloqueava o push.

## Regra principal

Nao use:

```bash
git push hf main:main --force
```

Tambem nao reescreva o historico de `origin/main`.

O deploy deve ser feito criando uma branch local baseada em `hf/main`, materializando nela o estado de `origin/main` e publicando um commit novo no remoto `hf`.

## Git Xet e binarios

O Hugging Face usa Xet para armazenar binarios. Para os assets binarios necessarios ao Space, use rastreamento especifico, nao padroes globais amplos.

Padroes permitidos neste projeto:

```text
frontend/public/brand/*.png
frontend/public/brand/*.ico
```

Esses arquivos sao necessarios para favicon, app icon e avatar. O social preview oficial deve continuar em SVG.

## Deploy automatizado

Use:

```bash
scripts/deploy_huggingface.sh
```

O script:

- exige working tree limpa na `main`;
- faz `fetch` de `origin` e `hf`;
- cria backup local de `hf/main`;
- cria uma worktree em `~/.cache/jarvis-hf-deploy`;
- materializa `origin/main` via `git archive`;
- aplica Git Xet/LFS somente aos assets binarios de marca;
- impede o retorno do PNG obsoleto;
- executa validacoes Python, dataset e frontend;
- cria commit de deploy;
- faz push para `hf/main`;
- nunca usa `git push --force` simples;
- nao grava nem imprime tokens.

## Comparacao apos o deploy

Depois do push, os hashes de `origin/main` e `hf/main` podem ser diferentes. Isso e esperado porque os historicos sao distintos.

Compare:

```bash
git fetch origin
git fetch hf
git diff --name-status origin/main hf/main
```

Diferencas aceitaveis:

- `.gitattributes` criado no ramo de deploy;
- ponteiros LFS/Xet para PNG/ICO necessarios.

Diferencas nao aceitaveis:

- codigo-fonte diferente;
- CSS diferente;
- assets SVG diferentes;
- documentacao funcional diferente;
- arquivos removidos sem justificativa.

## Validacao do Space

Teste:

```bash
curl -i https://teoz08-jarvis-academico.hf.space/api/status
curl -s https://teoz08-jarvis-academico.hf.space/api/status | python -m json.tool
```

Tambem valide no navegador:

- frontend carregando;
- tema escuro e claro;
- identidade violeta;
- navegacao;
- assets de marca;
- favicon;
- painel de evidencias;
- ausencia de erro 500.

Se a LLM externa falhar por certificado, token ou endpoint, trate isso separadamente do deploy. O Space pode estar publicado corretamente mesmo com indisponibilidade da API externa.

## Proibicoes

- Nao exponha tokens.
- Nao grave credenciais em arquivos.
- Nao use `--force` simples.
- Nao apague branches `backup/hf-*`.
- Nao reescreva `origin/main`.
- Nao adicione ZIPs, `.env`, `node_modules`, `.venv` ou screenshots ao deploy.
