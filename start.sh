#!/bin/bash
echo "[🔧 Installing Playwright browsers...]"
npx playwright install --with-deps

echo "[🚀 Launching Xclusive Engine...]"
gunicorn app:app --bind 0.0.0.0:$PORT
