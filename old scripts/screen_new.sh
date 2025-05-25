#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <screen_name> <command> [args...]"
    exit 1
fi

SCREEN_NAME="$1"
shift

# Create a detached screen session and run the command
screen -S "$SCREEN_NAME" -dm bash -c "$*"

#add the posibbility to see if the
