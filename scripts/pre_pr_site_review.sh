#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Pre-PR website review starting"

if [[ -f requirements.txt ]]; then
  echo "==> Installing Python dependencies for MkDocs"
  python -m pip install -r requirements.txt
fi

echo "==> Running website-facing analysis/build step"
python scripts/run_minimal_demo.py

echo "==> Building MkDocs site"
mkdocs build --strict

if [[ ! -d node_modules ]]; then
  echo "==> Installing Node dependencies"
  npm install
else
  echo "==> Ensuring Node dependencies are up to date"
  npm install --prefer-offline
fi

echo "==> Installing Playwright browser dependencies"
npx playwright install chromium

echo "==> Running Playwright site review"
npm run test:playwright

echo "==> Pre-PR website review passed"
