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

## Session Startup Commands

ascreen supports a configuration file named `profiles.ini` that allows you to define default startup commands for named screen sessions. This enables you to launch consistent, pre-configured environments just by referring to a session name — without typing the full command every time.

When you create a session using:
```bash
ascreen new <session_name> [optional command]
```
If no command is explicitly provided, ascreen will look up the command associated with that session name in the `profiles.ini` file and automatically run it.

## requirements

Python 3 installed. The script depends on `argparse` (standard with Python 3).

## run

You can just dounload the repository and run `ascreen.py`.

## Install as a global command
To Install `ascreen` as a global command:
1. Download the repository
2. Move the repository folder to a permenent place
3. Open the terminal in the `ascreen` folder and run:

```bash
bash pycmd_install.sh ascreen.py
```
## Uninstall
Open the terminal in the `ascreen` folder and run:
```bash
bash pycmd_uninstall.sh ascreen.py
```
