#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/home/matteo/Faculdade/IA/jarvis_academico}"
DEPLOY_DIR="${DEPLOY_DIR:-$HOME/.cache/jarvis-hf-deploy}"
DEPLOY_BRANCH="${DEPLOY_BRANCH:-hf-deploy}"
STAMP="$(date +%Y%m%d-%H%M%S)"

cd "$ROOT_DIR"

if [ -n "$(git status --short)" ]; then
  echo "ERRO: working tree local nao esta limpa." >&2
  git status --short >&2
  exit 1
fi

if [ "$(git branch --show-current)" != "main" ]; then
  echo "ERRO: execute a partir da branch main." >&2
  exit 1
fi

command -v git >/dev/null
command -v git-xet >/dev/null
command -v git-lfs >/dev/null
command -v npm >/dev/null

git fetch origin
git fetch hf

if [ "$(git rev-parse main)" != "$(git rev-parse origin/main)" ]; then
  echo "ERRO: main local nao esta alinhada com origin/main." >&2
  exit 1
fi

BACKUP_BRANCH="backup/hf-antes-do-deploy-$STAMP"
git branch "$BACKUP_BRANCH" hf/main
echo "Backup criado: $BACKUP_BRANCH"

if git worktree list --porcelain | grep -Fx "worktree $DEPLOY_DIR" >/dev/null; then
  git worktree remove "$DEPLOY_DIR" --force
fi

rm -rf "$DEPLOY_DIR"

if git show-ref --verify --quiet "refs/heads/$DEPLOY_BRANCH"; then
  LOCAL_BACKUP="backup/local-${DEPLOY_BRANCH}-$STAMP"
  git branch "$LOCAL_BACKUP" "$DEPLOY_BRANCH"
  echo "Backup da branch local criado: $LOCAL_BACKUP"
  git branch -D "$DEPLOY_BRANCH"
fi

git branch "$DEPLOY_BRANCH" hf/main
git worktree add "$DEPLOY_DIR" "$DEPLOY_BRANCH"

find "$DEPLOY_DIR" -mindepth 1 -maxdepth 1 ! -name ".git" -exec rm -rf {} +
git archive origin/main | tar -x -C "$DEPLOY_DIR"

cd "$DEPLOY_DIR"

git xet install
git lfs install --local
git xet track "frontend/public/brand/*.png"
git xet track "frontend/public/brand/*.ico"

test ! -e frontend/public/brand/social-preview-1200x630.png
test -f frontend/public/brand/social-preview.svg

if find . -name ".env" -o -name "node_modules" -o -name ".venv" -o -name "*.zip" | grep -q .; then
  echo "ERRO: arquivo ou diretorio proibido encontrado no deploy." >&2
  find . -name ".env" -o -name "node_modules" -o -name ".venv" -o -name "*.zip" >&2
  exit 1
fi

git add -A
git diff --cached --check

if git diff --cached --name-only --diff-filter=AM | grep -Ei '\.(png|jpe?g|gif|webp|ico|pdf|zip|pptx|npy|parquet)$'; then
  git diff --cached --name-only --diff-filter=AM |
    grep -Ei '\.(png|jpe?g|gif|webp|ico|pdf|zip|pptx|npy|parquet)$' |
    while IFS= read -r path; do
      git check-attr -a -- "$path"
      git show ":$path" | head -n 5 || true
    done
fi

if [ -f "$ROOT_DIR/.venv/bin/activate" ]; then
  # shellcheck source=/dev/null
  . "$ROOT_DIR/.venv/bin/activate"
fi

python -m compileall -q src web_api scripts app.py main.py
python -m pytest -q
python scripts/check_dataset.py

(
  cd frontend
  npm ci
  npm run build
)

git diff --cached --check

if git diff --cached --quiet; then
  echo "Nenhuma diferenca para publicar no Hugging Face."
else
  git commit -m "Sincroniza deploy com a versao atual do GitHub"
fi

git fetch hf
git push hf "$DEPLOY_BRANCH:main"

cd "$ROOT_DIR"
git fetch hf

echo "origin/main: $(git rev-parse --short origin/main)"
echo "hf/main:     $(git rev-parse --short hf/main)"
