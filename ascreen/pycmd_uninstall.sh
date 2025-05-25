#!/bin/bash

# Usage: ./uninstall_pycmd.sh /path/to/script.py

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

if [[ -L "$TARGET_PATH" ]]; then
    $USE_SUDO rm "$TARGET_PATH"
    echo "Uninstalled command '$CMD_NAME'."
else
    echo "Command '$CMD_NAME' not found at $TARGET_PATH."
fi
