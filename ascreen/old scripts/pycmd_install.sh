#!/bin/bash

# Usage: ./install_pycmd.sh /path/to/script.py

SCRIPT_PATH="$(realpath "$1")"
SCRIPT_NAME="$(basename "$SCRIPT_PATH")"
CMD_NAME="${SCRIPT_NAME%.*}"
TARGET_PATH="/usr/local/bin/$CMD_NAME"

if [[ ! -f "$SCRIPT_PATH" ]]; then
    echo "Error: Script '$SCRIPT_PATH' not found."
    exit 1
fi

chmod +x "$SCRIPT_PATH"
sudo ln -sf "$SCRIPT_PATH" "$TARGET_PATH"

echo "Installed '$CMD_NAME' as a global command."
