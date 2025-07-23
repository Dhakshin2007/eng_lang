# main.py

from interpreter.parser import parse_command
from interpreter.executor import Executor

import sys

def run_repl():
    print("Welcome to EnglishLang REPL. Type English commands.")
    executor = Executor()

    while True:
        try:
            line = input(">>> ")
            if line.lower() in ("exit", "quit"):
                break
            command = parse_command(line)
            executor.execute(command)
        except Exception as e:
            print(f"Error: {e}")

def run_file(filename):
    executor = Executor()
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                command = parse_command(line)
                executor.execute(command)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run_repl()
