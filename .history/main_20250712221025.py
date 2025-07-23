# main.py

from interpreter.parser import parse_command
from interpreter.executor import Executor

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

if __name__ == "__main__":
    run_repl()
