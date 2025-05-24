#!/bin/bash
set -e

export POETRY_PYPI_VERSION=0

echo "[🔧 Installing Python dependencies...]"
pip install -r requirements.txt

echo "[🎭 Installing Playwright Chromium...]"
python -m playwright install chromium

echo "[🚀 Launching Xclusive Engine...]"
python -m gunicorn app:app --bind 0.0.0.0:$PORT
