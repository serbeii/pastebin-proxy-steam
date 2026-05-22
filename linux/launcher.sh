#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$SCRIPT_DIR/../venv"

"$VENV/bin/python" "$SCRIPT_DIR/../proxy.py" &
PROXY_PID=$!

sleep 2

export HTTP_PROXY=http://127.0.0.1:8080
export HTTPS_PROXY=http://127.0.0.1:8080

"$@"

kill $PROXY_PID 2>/dev/null
