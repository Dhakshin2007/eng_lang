# interpreter/executor.py

from .memory import Memory
from .parser import ParsedCommand

class Executor:
    def __init__(self):
        self.memory = Memory()

    def execute(self, command: ParsedCommand):
        action = command.action
        args = command.args

        if action == "assign":
            self.memory.set(args["var"], args["value"])

        elif action == "add":
            current = self.memory.get(args["var"]) or 0
            self.memory.set(args["var"], current + args["value"])

        elif action == "print":
            print(args["text"])

        elif action == "if_print":
            value = self.memory.get(args["var"]) or 0
            if value > args["value"]:
                print(args["text"])

        elif action == "print_text":
            print(args["text"])

        elif action == "print_var":
            value = self.memory.get(args["var"])
        if value is not None:
            print(value)
        else:
            print(f"Variable '{args['var']}' not found.")

            print(f"Unknown command: {args.get('raw')}")

