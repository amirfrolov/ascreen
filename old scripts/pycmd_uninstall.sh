#!/bin/bash

# Usage: ./uninstall_pycmd.sh /path/to/script.py

SCRIPT_PATH="$(realpath "$1")"
SCRIPT_NAME="$(basename "$SCRIPT_PATH")"
CMD_NAME="${SCRIPT_NAME%.*}"
TARGET_PATH="/usr/local/bin/$CMD_NAME"

if [[ -L "$TARGET_PATH" ]]; then
    sudo rm "$TARGET_PATH"
    echo "Uninstalled command '$CMD_NAME'."
else
    echo "Command '$CMD_NAME' not found in /usr/local/bin."
fi
