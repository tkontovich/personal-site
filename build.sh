#!/usr/bin/env bash
# Build script for Vercel.
#
# This is not a Python app at runtime -- Django only renders the site to static
# HTML at build time -- so Vercel does not provision a Python environment for it.
# The system Python is uv-managed and refuses installs under PEP 668, so build
# inside a virtualenv we create ourselves.
set -euo pipefail

python3 -m venv .venv 2>/dev/null || uv venv .venv

if [ -x .venv/bin/pip ]; then
    .venv/bin/python -m pip install --disable-pip-version-check -r requirements.txt
else
    # A uv-created virtualenv has no pip of its own.
    uv pip install --python .venv/bin/python -r requirements.txt
fi

.venv/bin/python manage.py render_static
