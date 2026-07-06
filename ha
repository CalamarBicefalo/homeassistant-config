#!/usr/bin/env bash
# Root launcher for the support CLI: `ha <command>` runs `python -m ops` in the
# project's pipenv virtualenv, always from the repo root (so secrets/ and
# dashboard.yaml resolve regardless of where you invoke it).
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

venv="$(python3 -m pipenv --venv 2>/dev/null || true)"
if [[ -n "$venv" && -x "$venv/bin/python" ]]; then
  exec "$venv/bin/python" -m ops "$@"
fi
# Fall back to pipenv (also bootstraps the venv on first run).
exec python3 -m pipenv run python -m ops "$@"
