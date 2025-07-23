from parser import parse_command
from memory import Memory
from functions import FunctionManager

class Executor:
    def __init__(self):
        self.memory = Memory()
        self.functions = FunctionManager()

    def execute(self, command):
        action, args = command.action, command.args

        if action == "assign":
            try:
                self.memory.set(args["var"], int(args["value"]))
            except:
                self.memory.set(args["var"], args["value"])

        elif action == "print_text":
            print(args["text"])

        elif action == "print_var":
            print(self.memory.get(args["var"]))

        elif action == "print_combined":
            print(args["text"], self.memory.get(args["var"]))

        elif action == "add_to_var":
            val = self.memory.get(args["var"])
            self.memory.set(args["var"], val + args["value"])

        elif action == "input":
            self.memory.set(args["var"], input(args["prompt"] + ": "))

        elif action == "if_equals":
            if self.memory.get(args["left"]) == self.memory.get(args["right"]):
                print(args["text"])

        elif action == "if_not_equals":
            if self.memory.get(args["left"]) != self.memory.get(args["right"]):
                print(args["text"])

        elif action == "if_less_than":
            if self.memory.get(args["left"]) < self.memory.get(args["right"]):
                print(args["text"])

        elif action == "if_greater_than":
            if self.memory.get(args["left"]) > self.memory.get(args["right"]):
                print(args["text"])

        elif action == "while_loop":
            block = []
            print(">>> Enter loop block (type END to finish):")
            while True:
                line = input("... ")
                if line.strip().lower() == "end":
                    break
                block.append(line)

            while True:
                left_val = self.memory.get(args["left"])
                right_val = self.memory.get(args["right"]) if isinstance(args["right"], str) else args["right"]
                if left_val >= right_val:
                    break
                for line in block:
                    self.execute(parse_command(line))

        elif action == "list_declare":
            self.memory.set(args["name"], args["items"])

        elif action == "list_append":
            lst = self.memory.get(args["list"])
            if isinstance(lst, list):
                lst.append(args["item"])

        elif action == "list_index":
            lst = self.memory.get(args["list"])
            if isinstance(lst, list):
                idx = args["index"]
                if 0 <= idx < len(lst):
                    print(lst[idx])

        elif action == "list_length":
            lst = self.memory.get(args["list"])
            if isinstance(lst, list):
                self.memory.set(args["target"], len(lst))

        elif action == "for_loop":
            block = []
            print(">>> Enter loop block (type END to finish):")
            while True:
                line = input("... ")
                if line.strip().lower() == "end":
                    break
                block.append(line)
            for item in self.memory.get(args["list_var"]):
                self.memory.set(args["item_var"], item)
                for line in block:
                    self.execute(parse_command(line))

        elif action == "function_define_param":
            block = []
            print(">>> Enter function block (type END to finish):")
            while True:
                line = input("... ")
                if line.strip().lower() == "end":
                    break
                block.append(line)
            self.functions.define(args["name"], block, param=args["param"])

        elif action == "function_call_param":
            func = self.functions.get(args["name"])
            if func:
                self.memory.set(func["param"], args["arg"])
                for line in func["body"]:
                    self.execute(parse_command(line))

        elif action == "unknown":
            print("Unrecognized command:", args["line"])
