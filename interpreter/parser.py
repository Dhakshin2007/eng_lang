# interpreter/parser.py

import re

class ParsedCommand:
    def __init__(self, action, args):
        self.action = action
        self.args = args

def parse_command(line):
    line = line.strip()
    line_lower = line.lower()

    # Variable assignment
    if line_lower.startswith("let"):
        match_number = re.match(r"let (\w+) be (\d+)", line, re.IGNORECASE)
        if match_number:
            return ParsedCommand("assign", {
                "var": match_number[1],
                "value": int(match_number[2])
            })

        match_string = re.match(r'let (\w+) be "(.*)"', line, re.IGNORECASE)
        if match_string:
            return ParsedCommand("assign", {
                "var": match_string[1],
                "value": match_string[2]
            })

    # New: Add a and b into c
    match_add_vars = re.match(r"add (\w+) and (\w+) into (\w+)", line, re.IGNORECASE)
    if match_add_vars:
        return ParsedCommand("add_vars", {
            "var1": match_add_vars[1],
            "var2": match_add_vars[2],
            "target": match_add_vars[3]
        })

    # Arithmetic
    match_add = re.match(r"add (\d+) to (\w+)", line, re.IGNORECASE)
    if match_add:
        return ParsedCommand("add", {
            "value": int(match_add[1]),
            "var": match_add[2]
        })

    match_sub = re.match(r"subtract (\d+) from (\w+)", line, re.IGNORECASE)
    if match_sub:
        return ParsedCommand("subtract", {
            "value": int(match_sub[1]),
            "var": match_sub[2]
        })

    match_mul = re.match(r"multiply (\w+) by (\d+)", line, re.IGNORECASE)
    if match_mul:
        return ParsedCommand("multiply", {
            "var": match_mul[1],
            "value": int(match_mul[2])
        })

    match_div = re.match(r"divide (\w+) by (\d+)", line, re.IGNORECASE)
    if match_div:
        return ParsedCommand("divide", {
            "var": match_div[1],
            "value": int(match_div[2])
        })

    # Print: "something" and variable
    match_combo = re.match(r'(print|say) "(.*)" and (\w+)', line, re.IGNORECASE)
    if match_combo:
        return ParsedCommand("print_mixed", {
            "text": match_combo[2],
            "var": match_combo[3]
        })

    # Print: "something"
    match_text = re.match(r'(print|say) "(.*)"', line, re.IGNORECASE)
    if match_text:
        return ParsedCommand("print_text", {"text": match_text[2]})

    # Print: variable
    match_var = re.match(r'(print|say) (\w+)', line, re.IGNORECASE)
    if match_var:
        return ParsedCommand("print_var", {"var": match_var[2]})

    # Condition: If x is greater than 5, print "Yes"
    match_if = re.match(r'if (\w+) is greater than (\d+), print "(.*)"', line, re.IGNORECASE)
    if match_if:
        return ParsedCommand("if_print", {
            "var": match_if[1],
            "value": int(match_if[2]),
            "text": match_if[3]
        })

    # Loop: Repeat n times: print "..."
    match_loop = re.match(r'repeat (\d+) times: print "(.*)"', line, re.IGNORECASE)
    if match_loop:
        return ParsedCommand("repeat_print", {
            "count": int(match_loop[1]),
            "text": match_loop[2]
        })

    # Call function
    match_call = re.match(r"call (\w+)", line, re.IGNORECASE)
    if match_call:
        return ParsedCommand("call_function", {
            "name": match_call[1]
        })
    
        # Ask for input
    match_input = re.match(r'ask "(.*)" into (\w+)', line, re.IGNORECASE)
    if match_input:
        return ParsedCommand("input", {
            "prompt": match_input[1],
            "var": match_input[2]
        })
    
        # Equals condition
    match_eq = re.match(r'if (\w+) equals (\w+), print "(.*)"', line, re.IGNORECASE)
    if match_eq:
        return ParsedCommand("if_equals", {
            "left": match_eq[1],
            "right": match_eq[2],
            "text": match_eq[3]
        })

    # Not equals condition
    match_neq = re.match(r'if (\w+) not equals (\w+), print "(.*)"', line, re.IGNORECASE)
    if match_neq:
        return ParsedCommand("if_not_equals", {
            "left": match_neq[1],
            "right": match_neq[2],
            "text": match_neq[3]
        })

    # Less than
    match_lt = re.match(r'if (\w+) is less than (\w+), print "(.*)"', line, re.IGNORECASE)
    if match_lt:
        return ParsedCommand("if_less_than", {
            "left": match_lt[1],
            "right": match_lt[2],
            "text": match_lt[3]
        })
    
        # While loop
        # While loop (supports number literals or variable)
    match_while = re.match(r'while (\w+) is less than (\w+|\d+):', line, re.IGNORECASE)
    if match_while:
        right = match_while[2]
        # Convert to int if it's a number
        try:
            right_val = int(right)
        except ValueError:
            right_val = right  # keep as variable
        return ParsedCommand("while_loop", {
            "left": match_while[1],
            "right": right_val
        })

    # List declaration
    match_list = re.match(r'list (\w+): (.+)', line, re.IGNORECASE)
    if match_list:
        items = [item.strip().strip('"') for item in match_list[2].split(",")]
        return ParsedCommand("list_declare", {
            "name": match_list[1],
            "items": items
        })

    # For each loop
    match_for = re.match(r'for each (\w+) in (\w+):', line, re.IGNORECASE)
    if match_for:
        return ParsedCommand("for_loop", {
            "item_var": match_for[1],
            "list_var": match_for[2]
        })
    # Index from list
    match_index = re.match(r'print (\w+) at (\d+)', line, re.IGNORECASE)
    if match_index:
        return ParsedCommand("list_index", {
            "list": match_index[1],
            "index": int(match_index[2])
        })

    # Append to list
    match_append = re.match(r'add "(.*)" to (\w+)', line, re.IGNORECASE)
    if match_append:
        return ParsedCommand("list_append", {
            "item": match_append[1],
            "list": match_append[2]
        })

    # Get length of list
    match_length = re.match(r'length of (\w+) into (\w+)', line, re.IGNORECASE)
    if match_length:
        return ParsedCommand("list_length", {
            "list": match_length[1],
            "target": match_length[2]
        })

    # Define function with param
    match_func_def = re.match(r'define (\w+) (\w+):', line, re.IGNORECASE)
    if match_func_def:
        return ParsedCommand("function_define_param", {
            "name": match_func_def[1],
            "param": match_func_def[2]
        })

    # Call function with param
    match_func_call = re.match(r'call (\w+) with "(.*)"', line, re.IGNORECASE)
    if match_func_call:
        return ParsedCommand("function_call_param", {
            "name": match_func_call[1],
            "arg": match_func_call[2]
        })





    return ParsedCommand("unknown", {"raw": line})
