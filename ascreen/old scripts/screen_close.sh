#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <screen_name>"
    exit 1
fi

SCREEN_NAME="$1"

# Function to check if screen session exists
screen_exists() {
#     screen -list | grep -q "[.]$SCREEN_NAME"
    screen -ls "$SCREEN_NAME" > /dev/null
}

if ! screen_exists; then
    echo "No screen session named '$SCREEN_NAME' found to close."
    exit 1
fi

# Send Ctrl+C
screen -S "$SCREEN_NAME" -X stuff $'\003'

# Wait up to 1 second, checking every 0.1 sec
for i in {1..30}; do
    sleep 0.1
    if ! screen_exists; then
        echo "Session '$SCREEN_NAME' terminated with Ctrl+C."
        exit 0
    fi
done

# If still running, send quit
echo "Session '$SCREEN_NAME' still running. Sending 'quit'."
screen -S "$SCREEN_NAME" -X quit

#remove dead screens
screen -wipe "$SCREEN_NAME" > /dev/null
