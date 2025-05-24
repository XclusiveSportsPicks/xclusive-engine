#!/bin/bash
set -e  # Exit on error

echo "[🔧 Installing Python dependencies...]"
pip install -r requirements.txt

echo "[🎭 Installing Playwright Chromium...]"
python -m playwright install chromium

echo "[🚀 Launching Xclusive Engine...]"
gunicorn app:app --bind 0.0.0.0:$PORT
