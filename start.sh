#!/bin/bash
echo "[🔧 Installing dependencies...]"
pip install -r requirements.txt
echo "[🎭 Installing Playwright browsers...]"
npx playwright install
echo "[🚀 Launching Xclusive Engine...]"
gunicorn app:app
