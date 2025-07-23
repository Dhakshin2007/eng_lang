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

        elif action == "input":
            user_input = input(args["prompt"] + " ")
            self.memory.set(args["var"], user_input)
        
        elif action == "if_equals":
            left = self.memory.get(args["left"])
            right = self.memory.get(args["right"])
            if left == right:
                print(args["text"])

        elif action == "if_not_equals":
            left = self.memory.get(args["left"])
            right = self.memory.get(args["right"])
            if left != right:
                print(args["text"])

        elif action == "if_less_than":
            left = self.memory.get(args["left"])
            right = self.memory.get(args["right"])
            if isinstance(left, (int, float)) and isinstance(right, (int, float)) and left < right:
                print(args["text"])

        elif action == "while_loop":
            right = args["right"]
            if isinstance(right, str):
                right_val = self.memory.get(right)
                try:
                    right_val = int(right_val)
                except:
                    print("Error: Invalid right-hand side in while loop.")
                    return
            else:
                right_val = right

        elif action == "list_declare":
            self.memory.set(args["name"], args["items"])

        elif action == "for_loop":
            list_items = self.memory.get(args["list_var"])
            if not isinstance(list_items, list):
                print(f"Error: '{args['list_var']}' is not a list.")
                return

            block = []
            print(">>> Enter loop block (type END to finish):")
            while True:
                line = input("... ")
                if line.strip().lower() == "end":
                    break
                block.append(line)

            for item in list_items:
                self.memory.set(args["item_var"], item)
                for bline in block:
                    command = parse_command(bline)
                    self.execute(command)

        elif action == "list_index":
            lst = self.memory.get(args["list"])
            idx = args["index"]
            if isinstance(lst, list) and 0 <= idx < len(lst):
                print(lst[idx])
            else:
                print("Error: Invalid index or list.")

        elif action == "list_append":
            lst = self.memory.get(args["list"])
            if isinstance(lst, list):
                lst.append(args["item"])
            else:
                print(f"Error: '{args['list']}' is not a list.")

        elif action == "list_length":
            lst = self.memory.get(args["list"])
            if isinstance(lst, list):
                self.memory.set(args["target"], len(lst))
            else:
                print(f"Error: '{args['list']}' is not a list.")

        elif action == "function_define_param":
            block = []
            print(">>> Enter function block (type END to finish):")
            while True:
                line = input("... ")
                if line.strip().lower() == "end":
                    break
                block.append(line)
            self.functions[args["name"]] = {
                "param": args["param"],
                "body": block
            }

        elif action == "function_call_param":
            func = self.functions.get(args["name"])
            if not func:
                print(f"Error: Function '{args['name']}' not found.")
                return
            self.memory.set(func["param"], args["arg"])
            for line in func["body"]:
                command = parse_command(line)
                self.execute(command)




            block = []
            print(">>> Enter loop block (type END to finish):")
            while True:
                line = input("... ")
                if line.strip().lower() == "end":
                    break
                block.append(line)

            # Actual loop execution
            while True:
                left_val = self.memory.get(args["left"])
                if not isinstance(left_val, (int, float)):
                    try:
                        left_val = int(left_val)
                    except:
                        break
                if left_val >= right:
                    break
                for bline in block:
                    command = parse_command(bline)
                    self.execute(command)




    def register_function(self, header_line, body_lines):
        match = header_line.strip().lower().split()
        if len(match) == 2 and match[0] == "define":
            func_name = match[1].replace(":", "")
            self.functions.define(func_name, body_lines)
        else:
            print(f"Invalid function definition: {header_line}")
