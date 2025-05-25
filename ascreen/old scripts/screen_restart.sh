#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <screen_name> <command> [args...]"
    exit 1
fi

SCREEN_NAME="$1"
shift

bash screen_close.sh "$SCREEN_NAME"

# Create a detached screen session and run the command
screen -S "$SCREEN_NAME" -dm bash -c "$*"
echo "session '$SCREEN_NAME' created successfully"
#add the posibbility to see if the
