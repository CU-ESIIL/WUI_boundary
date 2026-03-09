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
  docs/assets/figures/real_fixed_boundary_scaling.png
  docs/assets/figures/real_resolution_rebuild_scaling.png
  docs/assets/data/real_fixed_boundary_scaling.csv
  docs/assets/data/real_resolution_rebuild_scaling.csv
)

echo "==> Verifying required real-data docs assets are present"
for path in "${required_docs_assets[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "ERROR: Missing required docs real-data asset: $path" >&2
    echo "Run scripts/run_streaming_wui_scaling.py --bbox=-105.292,40.004,-105.236,40.047 --outdir outputs/real_data_demo --publish-doc-assets" >&2
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
