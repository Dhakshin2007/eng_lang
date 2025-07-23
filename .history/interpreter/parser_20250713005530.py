import re

class ParsedCommand:
    def __init__(self, action, args):
        self.action = action
        self.args = args

def parse_command(line):
    line = line.strip()

    if line.lower().startswith("let"):
        match = re.match(r'let (\w+) be (.+)', line, re.IGNORECASE)
        if match:
            return ParsedCommand("assign", {"var": match[1], "value": match[2]})

    if line.lower().startswith("print"):
        match = re.match(r'print "(.*)" and (\w+)', line, re.IGNORECASE)
        if match:
            return ParsedCommand("print_combined", {"text": match[1], "var": match[2]})
        match2 = re.match(r'print (\w+)', line, re.IGNORECASE)
        if match2:
            return ParsedCommand("print_var", {"var": match2[1]})
        match3 = re.match(r'print "(.*)"', line, re.IGNORECASE)
        if match3:
            return ParsedCommand("print_text", {"text": match3[1]})

    match_add = re.match(r'add (\d+) to (\w+)', line, re.IGNORECASE)
    if match_add:
        return ParsedCommand("add_to_var", {"value": int(match_add[1]), "var": match_add[2]})

    match_input = re.match(r'ask "(.*)" into (\w+)', line, re.IGNORECASE)
    if match_input:
        return ParsedCommand("input", {"prompt": match_input[1], "var": match_input[2]})

    match_eq = re.match(r'if (\w+) equals (\w+), print "(.*)"', line, re.IGNORECASE)
    if match_eq:
        return ParsedCommand("if_equals", {"left": match_eq[1], "right": match_eq[2], "text": match_eq[3]})

    match_neq = re.match(r'if (\w+) not equals (\w+), print "(.*)"', line, re.IGNORECASE)
    if match_neq:
        return ParsedCommand("if_not_equals", {"left": match_neq[1], "right": match_neq[2], "text": match_neq[3]})

    match_gt = re.match(r'if (\w+) is greater than (\w+), print "(.*)"', line, re.IGNORECASE)
    if match_gt:
        return ParsedCommand("if_greater_than", {"left": match_gt[1], "right": match_gt[2], "text": match_gt[3]})

    match_lt = re.match(r'if (\w+) is less than (\w+), print "(.*)"', line, re.IGNORECASE)
    if match_lt:
        return ParsedCommand("if_less_than", {"left": match_lt[1], "right": match_lt[2], "text": match_lt[3]})

    match_while = re.match(r'while (\w+) is less than (\w+|\d+):', line, re.IGNORECASE)
    if match_while:
        right = match_while[2]
        try:
            right_val = int(right)
        except:
            right_val = right
        return ParsedCommand("while_loop", {"left": match_while[1], "right": right_val})

    match_list = re.match(r'list (\w+): (.+)', line, re.IGNORECASE)
    if match_list:
        items = [item.strip().strip('"') for item in match_list[2].split(",")]
        return ParsedCommand("list_declare", {"name": match_list[1], "items": items})

    match_for = re.match(r'for each (\w+) in (\w+):', line, re.IGNORECASE)
    if match_for:
        return ParsedCommand("for_loop", {"item_var": match_for[1], "list_var": match_for[2]})

    match_index = re.match(r'print (\w+) at (\d+)', line, re.IGNORECASE)
    if match_index:
        return ParsedCommand("list_index", {"list": match_index[1], "index": int(match_index[2])})

    match_append = re.match(r'add "(.*)" to (\w+)', line, re.IGNORECASE)
    if match_append:
        return ParsedCommand("list_append", {"item": match_append[1], "list": match_append[2]})

    match_length = re.match(r'length of (\w+) into (\w+)', line, re.IGNORECASE)
    if match_length:
        return ParsedCommand("list_length", {"list": match_length[1], "target": match_length[2]})

    match_func_def = re.match(r'define (\w+) (\w+):', line, re.IGNORECASE)
    if match_func_def:
        return ParsedCommand("function_define_param", {"name": match_func_def[1].lower(), "param": match_func_def[2]})

    match_func_call = re.match(r'call (\w+) with "?([\w\s]+)?"?', line, re.IGNORECASE)
    if match_func_call:
        return ParsedCommand("function_call_param", {"name": match_func_call[1].lower(), "arg": match_func_call[2]})

    return ParsedCommand("unknown", {"line": line})
