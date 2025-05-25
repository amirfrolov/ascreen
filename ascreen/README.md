# ascreen

`ascreen` is a specialized wrapper around GNU Screen, designed to enhance session management by session names and profiles. It allows more controlled and automated handling of screen sessions, including graceful exits, bulk operations, and command binding to session names.

## Features

- List all screen sessions by name.
- Attach to a named session easily.
- Create new sessions and run predefined or custom commands.
- Restart sessions by closing and recreating them with commands.
- Stop sessions gracefully by sending Ctrl+C before quitting.
- Stop all sessions or only unnamed sessions in bulk.
- Wipe dead (defunct) screen sessions.
- Bind commands to session names via `profiles.ini` — when creating a session without a command, it automatically runs the associated command.

## Why use `ascreen`?

- If you use GNU Screen and want better session automation and management.
- Graceful shutdown of sessions to avoid orphan processes.
- Automated workflows by associating session names with startup commands.
- Useful in legacy environments or when tmux is unavailable or unwanted.

## Installation

Clone the repo and ensure you have Python 3 installed. The script depends on `argparse` (standard with Python 3).

```bash
git clone https://github.com/yourusername/ascreen.git
cd ascreen
chmod +x ascreen.py
./ascreen.py <command> [args]
