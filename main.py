# main.py

import sys
from interpreter.parser import parse_command
from interpreter.executor import Executor
from interpreter.functions import FunctionManager

def run_repl():
    print("🔥 Welcome to EnglishLang REPL. Type 'exit' to quit.")
    executor = Executor()
    while True:
        try:
            line = input(">>> ")
            if line.strip().lower() in ("exit", "quit"):
                break
            command = parse_command(line)
            executor.execute(command)
        except Exception as e:
            print(f"Error: {e}")

def run_file(filename):
    executor = Executor()
    with open(filename, "r") as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Check if defining a function
        if line.lower().startswith("define"):
            func_lines = []
            header = line
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].startswith("\t")):
                func_lines.append(lines[i].strip())
                i += 1
            executor.register_function(header, func_lines)
        else:
            command = parse_command(line)
            executor.execute(command)
            i += 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run_repl()
