#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Pre-PR website review starting"

echo "==> Installing canonical project runtime dependencies"
python -m pip install -e .

if [[ -f requirements.txt ]]; then
  echo "==> Installing documentation-only dependencies"
  python -m pip install -r requirements.txt
fi

echo "==> Running website-facing analysis/build step"
python scripts/run_minimal_demo.py


required_docs_assets=(
  docs/assets/figures/real_interface_scaling.png
  docs/assets/data/real_interface_scaling.csv
)

echo "==> Verifying required real-data docs assets are present"
for path in "${required_docs_assets[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "ERROR: Missing required docs real-data asset: $path" >&2
    echo "Run scripts/run_streaming_wui_scaling.py --bbox=-105.271,40.018,-105.268,40.021 --outdir outputs/real_data_demo --resolutions=10,20,40,80 --adj-buffer=30 --publish-doc-assets" >&2
    exit 1
  fi
done

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
