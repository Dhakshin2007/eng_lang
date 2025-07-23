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

        elif action == "repeat_print":
            for _ in range(args["count"]):
                print(args["text"])

        else:
            print(f"Unknown command: {args.get('raw')}")
