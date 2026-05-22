#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/../venv"

echo "Creating virtual environment..."
python3 -m venv "$VENV"

chmod +x "$SCRIPT_DIR/launcher.sh"

echo "Generating Steam launch option..."
LAUNCHER="$SCRIPT_DIR/launcher.sh"
echo "\"$LAUNCHER\" %command%" > "$SCRIPT_DIR/../steam_launch_option.txt"

echo ""
echo "============================================"
echo "Paste this into Steam Launch Options:"
cat "$SCRIPT_DIR/../steam_launch_option.txt"
echo "============================================"
