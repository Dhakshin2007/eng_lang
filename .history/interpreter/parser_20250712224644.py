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

    return ParsedCommand("unknown", {"raw": line})
