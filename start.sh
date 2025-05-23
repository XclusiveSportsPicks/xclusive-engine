#!/bin/bash
echo "[🔧 Installing Playwright browsers...]"
playwright install
echo "[🚀 Launching Xclusive Engine...]"
python app.py
