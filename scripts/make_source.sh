#!/usr/bin/env bash
set -euo pipefail
git2md src/readme_maker \
  --ignore __init__.py __pycache__ \
  __about__.py logging_config.py py.typed utils \
  templates \
  --output SOURCE.md
