# interpreter/executor.py

from .memory import Memory
from .functions import FunctionManager
from .parser import ParsedCommand, parse_command

class Executor:
    def __init__(self):
        self.memory = Memory()
        self.functions = FunctionManager()

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

        elif action == "add_vars":
            v1 = self.memory.get(args["var1"])
            v2 = self.memory.get(args["var2"])
            if v1 is None or v2 is None:
                print("Error: One or both variables not found.")
            elif not isinstance(v1, (int, float)) or not isinstance(v2, (int, float)):
                print("Error: Can only add numeric variables.")
            else:
                self.memory.set(args["target"], v1 + v2)

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
            print(args["text"] + str(value) if value is not None else args["text"] + "undefined")

        elif action == "if_print":
            value = self.memory.get(args["var"]) or 0
            if isinstance(value, (int, float)) and value > args["value"]:
                print(args["text"])

        elif action == "repeat_print":
            for _ in range(args["count"]):
                print(args["text"])

        elif action == "call_function":
            func_body = self.functions.get(args["name"])
            if func_body:
                for line in func_body:
                    command = parse_command(line)
                    self.execute(command)
            else:
                print(f"Function '{args['name']}' not found.")

        elif action == "unknown":
            print(f"Unrecognized command: {args.get('raw')}")

            

    def register_function(self, header_line, body_lines):
        match = header_line.strip().lower().split()
        if len(match) == 2 and match[0] == "define":
            func_name = match[1].replace(":", "")
            self.functions.define(func_name, body_lines)
        else:
            print(f"Invalid function definition: {header_line}")
