#!/usr/bin/env bash
set -euo pipefail
#git2md src/github_is_my_cms \
#  --ignore __init__.py __pycache__ \
#  __about__.py logging_config.py py.typed utils \
#  --output SOURCE.md

git2md . \
  --ignore __init__.py __pycache__ \
  .venv \
  dead_code data docs scripts \
  __about__.py logging_config.py py.typed utils \
  .gitignore  .pre-commit-config.yaml .ruff_cache README* \
  LICENSE SOURCE.md \
  .cache \
  uv.lock \
  templates swagger \
  --output SOURCE.md
