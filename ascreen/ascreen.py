#!/usr/bin/python
import sys
import argparse
import subprocess
from dataclasses import dataclass, field
import time
import os

TIME_OUT = 1
import configparser

def get_screen_command(screen_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(script_dir, "profiles.ini")
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
        return config.get("commands", screen_name, fallback=None)
    except Exception as e:
        print(f"Error reading {config_path}: {e}")
        return None

# import yaml
# def get_screen_command(screen_name, config_path="profiles.yaml"):
#     try:
#         with open(config_path, 'r') as f:
#             data = yaml.safe_load(f)
#         return data.get(screen_name, None)
#     except FileNotFoundError:
#         print(f"Config file {config_path} not found.")
#         return None
#     except yaml.YAMLError as e:
#         print(f"YAML parsing error: {e}")
#         return None

def subprocess_run(args : list, capture_text_output=True):
    return subprocess.run(args, capture_output=capture_text_output, text=capture_text_output)
    #returncode, stdout, stderr

import shlex

def new_screen(session_name, screen_command=None, args=None):
    if args is None:
        args = []
    if screen_command is None:
        screen_command = get_screen_command(session_name)
        if not screen_command:
            pass
            # print(f"Screen '{session_name}' not found in profiles.ini")
            # return

    if screen_command:
        args = [shlex.quote(arg) for arg in args]
        full_cmd = shlex.quote(f"{screen_command} {' '.join(args)}")
        command = f'screen -S {session_name} -dm bash -c {full_cmd}'
    else:
        command = f'screen -S {session_name}'

    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Failed to launch screen '{session_name}'")


# def new_screen(session_name, screen_command, args=[]):
#     if screen_command == None:
#         screen_command = get_screen_command(session_name)
#         if not screen_command:
#             print(f'Screen {session_name} not found in profiles.yaml')
#             return
#     args = [i.replace(" ", "\\ ") for i in args]
#     command = f'screen -S {session_name} -dm bash -c "{screen_command} {" ".join(args)}" '
#     subprocess.run(command, shell=True)

@dataclass
class Session:
    full_id : str
    status : str
    name : str
    pid : str

    def is_dead(self):
        return "dead" in self.status.lower()

    def is_running(self):
        path = subprocess_run(["pstree", "-p", self.pid]).stdout
        if not path:
            return False
        path = path.replace("───", "---")
        process_name = path.split("---")[-1].split("(", 1)[0]
        return path.count("---") > 1 or process_name != "bash"


class Sessions:
    def __init__(self, session_name = ""):
        self.session_name = session_name
        #get the sessions
        self.exact_match_flag = True
        self.get_sessions()

    def get_sessions(self):
        self.sessions = list()
        self.sessions_data_str = str()
        result = subprocess.run(['screen', '-ls', self.session_name], capture_output=True, text=True)
        if not result.returncode:
            lines = result.stdout.split("\n")
            self.sessions_data_str = lines[-2]
            # print(lines)
            for session_line in lines[1:-2]:
                if session_line[0] != "\t":
                    continue
                session_line_data = session_line.split(maxsplit=1)
                full_id = session_line_data[0]
                status = session_line_data[1]
                # print(1, session_line_data)

                full_id_parts = full_id.split(".", 1)
                pid = full_id_parts[0]
                name = full_id_parts[1]
                # Session(full_id, status)
                s = Session(full_id, status, name, pid)
                if not self.exact_match_flag:
                    self.sessions.append(s)
                elif not self.session_name:
                    self.sessions.append(s)
                elif self.session_name == name or self.session_name == full_id:
                    self.sessions.append(s)

    def filter_to_unnamed(self):
        self.sessions = [s for s in self.sessions if s.full_id.count(".") > 1]

    def __len__(self):
        return len(self.sessions)

    def wipe(self):
        wipe_flag = False
        for i in self.sessions:
            # print(i)
            if i.is_dead(): # remove dead screens
                wipe_flag = True
                print("Wipes:", i.full_id)
                subprocess_run(['screen', '-wipe', i.full_id])

        # if wipe_flag:
        #     # Wait up to 1 second, checking every 0.1 sec
        #     time_end = time.time() + TIME_OUT
        #     while wait_list and time.time() < time_end:
        #         if wait_list:
        #             time.sleep(0.1)
        #         self.get_sessions()
        #         wait_list = [i for i in self.sessions if i.is_dead()]
        #         if wait_list:
        #             print("Waiting for:", ", ".join([i.full_id for i in wait_list]))

    def stop(self):
        if not self:
            print(f"No screen session named '{self.session_name}' found to close.")
            return

        wait_list = list()
        for i in self.sessions:
            if i.is_dead(): # remove dead screens
                print("Wipes:", i.full_id)
                subprocess_run(['screen', '-wipe', i.full_id])
            elif i.is_running(): # Send Ctrl+C
            # elif False:
                wait_list.append(i)
                print("Ctrl+C:", i.full_id)
                subprocess_run(['screen', '-S', i.full_id, "-X", "stuff", "$'\003'"])
            else: #send quit
                print("Quits:", i.full_id)
                subprocess_run(['screen', '-S', i.full_id, "-X", "quit"])


        # Wait up to 1 second, checking every 0.1 sec
        time_end = time.time() + TIME_OUT
        while wait_list and time.time() < time_end:
            if wait_list:
                time.sleep(0.1)
            wait_list = [i for i in wait_list if i.is_running()]
            if wait_list:
                print("Waiting for:", ", ".join([i.full_id for i in wait_list]))

        # self.get_sessions()
        # If still running, send quit
        # for i in self.sessions:
        for i in wait_list:
            print("Force quits:", i.full_id)
            subprocess_run(['screen', '-S', i.full_id, "-X", "quit"])

    def exact_match(self):
        self.exact_match_flag = True
        if not self.session_name:
            self.sessions = list()
        else:
            self.sessions = [i for i in self.sessions if i.name == self.session_name]

def action_parser_add_subject_name(arg_parser, default=None):
    arg_name = 'session_name'
    arg_help = 'Name or id of the screen session'
    arg_type = str

    if default == None:
        arg_parser.add_argument(arg_name, type=arg_type, help=arg_help)
    else: # Optional positional argument
        arg_parser.add_argument(arg_name, nargs='?', default=default, type=arg_type, help=arg_help)

def action_parser_add_cmd_command(arg_parser):
    arg_parser.add_argument(
    "screen_command",
    type=str,
    nargs="?",
    default=None,
    help="Command to run. Can include multiple commands if passed in quotes and separated by ';'"
    )
    arg_parser.add_argument('args', nargs=argparse.REMAINDER, help='arguments to pass')
    return

def main():
    parser = argparse.ArgumentParser(prog='ascreen', description="Manage screen sessions by name")
    subparsers = parser.add_subparsers(dest='command')

    arg_parser = subparsers.add_parser('ls', help='Lists all the screen sessions.')

    arg_parser = subparsers.add_parser('attach', help='Attaches a session.')
    action_parser_add_subject_name(arg_parser)

    arg_parser = subparsers.add_parser('r', help='Attaches a session.')
    action_parser_add_subject_name(arg_parser)

    arg_parser = subparsers.add_parser('new', help='Creates a new session, and sends a command.')
    action_parser_add_subject_name(arg_parser)
    action_parser_add_cmd_command(arg_parser)
    # arg_parser.add_argument("screen_command", type=str, help= "Command to run, can run multiple commands if passes in quotes, and have ';' between them")
    # arg_parser.add_argument('args', nargs=argparse.REMAINDER, help='arguments to pass')

    arg_parser = subparsers.add_parser('restart', help='Closes a session, recreates it,  and sends a command.')
    action_parser_add_subject_name(arg_parser)
    action_parser_add_cmd_command(arg_parser)

    arg_parser = subparsers.add_parser('stop', help='Stops a session: sends ctrl+C, quits, and wipes')
    action_parser_add_subject_name(arg_parser)

    arg_parser = subparsers.add_parser('stop-all', help='Stops all of the screens')

    arg_parser = subparsers.add_parser('stop-unnamed', help='Stops all of the unnamed screens')

    arg_parser = subparsers.add_parser('wipe', help='Wipes all dead screens')
    action_parser_add_subject_name(arg_parser, "")

    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    try:
        session_name = args.session_name
    except AttributeError:
        session_name = ""

    sessions = Sessions(session_name)

    #handle the args
    if args.command == 'ls':
        subprocess_run(['screen', '-ls'], False)

    elif args.command == 'stop-all':
        sessions.stop()

    elif args.command == 'stop-unnamed':
        sessions.filter_to_unnamed()
        sessions.stop()

    elif args.command == 'attach' or args.command == 'r':
        subprocess_run(["screen", "-r", session_name], False)

    elif args.command == 'new':
        sessions.wipe()
        if sessions:
            print("There is already a running ssesion named:", session_name)
        else:
            new_screen(session_name, args.screen_command, args.args)

    elif args.command == 'restart':
        sessions.stop()
        new_screen(session_name, args.screen_command, args.args)

    elif args.command == 'stop':
        sessions.stop()

    elif args.command == "wipe":
        sessions.wipe()

if __name__ == "__main__":
    main()
