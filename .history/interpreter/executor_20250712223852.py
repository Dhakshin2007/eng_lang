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

        elif action == "subtract":
            current = self.memory.get(args["var"]) or 0
            self.memory.set(args["var"], current - args["value"])

        elif action == "multiply":
            current = self.memory.get(args["var"]) or 0
            self.memory.set(args["var"], current * args["value"])

        elif action == "divide":
            current = self.memory.get(args["var"]) or 0
            if args["value"] != 0:
                self.memory.set(args["var"], current // args["value"])
            else:
                print("Cannot divide by zero.")

        elif action == "print_text":
            print(args["text"])

        elif action == "print_var":
            value = self.memory.get(args["var"])
            if value is not None:
                print(value)
            else:
                print(f"Variable '{args['var']}' not found.")

        elif action == "print_mixed":
            value = self.memory.get(args["var"])
            if value is not None:
                print(args["text"] + str(value))
            else:
                print(args["text"] + "undefined")

        elif action == "if_print":
            value = self.memory.get(args["var"]) or 0
            if isinstance(value, (int, float)) and value > args["value"]:
                print(args["text"])

        elif action == "repeat_print":
            for _ in range(args["count"]):
                print(args["text"])

        else:
            print(f"Unrecognized command: {args.get('raw')}")
