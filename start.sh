#!/bin/bash
echo "[🔧 Installing dependencies...]"
pip install -r requirements.txt

echo "[🎭 Installing Playwright Chromium only...]"
npx playwright install chromium

echo "[🚀 Launching Xclusive Engine...]"
gunicorn app:app --bind 0.0.0.0:$PORT
