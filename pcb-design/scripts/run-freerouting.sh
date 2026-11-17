#!/usr/bin/env bash
# run-freerouting.sh: Helper to launch Freerouting with a Specctra DSN file.
# Usage: ./run-freerouting.sh <path-to-board.dsn>

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <path-to-board.dsn>"
    echo "Export a .dsn file in KiCad PCB Editor via: File -> Export -> Specctra DSN"
    exit 1
fi

DSN_FILE="$1"

if ! command -v freerouting >/dev/null 2>&1; then
    echo "Error: freerouting is not found in PATH." >&2
    exit 1
fi

if [ ! -f "$DSN_FILE" ]; then
    echo "Error: DSN file '$DSN_FILE' not found." >&2
    exit 1
fi

echo "==> Launching Freerouting with $DSN_FILE..."
freerouting -de "$DSN_FILE"
