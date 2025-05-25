#!/bin/bash

# Usage: ./install_pycmd.sh /path/to/script.py

SCRIPT_PATH="$(realpath "$1")"
SCRIPT_NAME="$(basename "$SCRIPT_PATH")"
CMD_NAME="${SCRIPT_NAME%.*}"

# Detect if running in Termux
if [[ "$PREFIX" == *termux* ]]; then
    TARGET_PATH="$PREFIX/bin/$CMD_NAME"
    USE_SUDO=""
else
    TARGET_PATH="/usr/local/bin/$CMD_NAME"
    USE_SUDO="sudo"
fi

if [[ ! -f "$SCRIPT_PATH" ]]; then
    echo "Error: Script '$SCRIPT_PATH' not found."
    exit 1
fi

chmod +x "$SCRIPT_PATH"
$USE_SUDO ln -sf "$SCRIPT_PATH" "$TARGET_PATH"

echo "Installed '$CMD_NAME' as a global command at $TARGET_PATH."
