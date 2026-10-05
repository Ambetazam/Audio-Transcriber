#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo
echo "Installation complete. Try:"
echo "  audio-transcriber --help"
echo "  audio-transcriber recording.m4a --language es"
