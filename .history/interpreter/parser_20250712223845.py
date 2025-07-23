# interpreter/parser.py

import re

class ParsedCommand:
    def __init__(self, action, args):
        self.action = action
        self.args = args

def parse_command(line):
    line = line.strip()
    line_lower = line.lower()

    # Let number
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

    # Add
    match_add = re.match(r"add (\d+) to (\w+)", line, re.IGNORECASE)
    if match_add:
        return ParsedCommand("add", {
            "value": int(match_add[1]),
            "var": match_add[2]
        })

    # Subtract
    match_subtract = re.match(r"subtract (\d+) from (\w+)", line, re.IGNORECASE)
    if match_subtract:
        return ParsedCommand("subtract", {
            "value": int(match_subtract[1]),
            "var": match_subtract[2]
        })

    # Multiply
    match_multiply = re.match(r"multiply (\w+) by (\d+)", line, re.IGNORECASE)
    if match_multiply:
        return ParsedCommand("multiply", {
            "var": match_multiply[1],
            "value": int(match_multiply[2])
        })

    # Divide
    match_divide = re.match(r"divide (\w+) by (\d+)", line, re.IGNORECASE)
    if match_divide:
        return ParsedCommand("divide", {
            "var": match_divide[1],
            "value": int(match_divide[2])
        })

    # Print "text" and variable
    match_combo = re.match(r'(print|say) "(.*)" and (\w+)', line, re.IGNORECASE)
    if match_combo:
        return ParsedCommand("print_mixed", {
            "text": match_combo[2],
            "var": match_combo[3]
        })

    # Print "text"
    match_print_text = re.match(r'(print|say) "(.*)"', line, re.IGNORECASE)
    if match_print_text:
        return ParsedCommand("print_text", {"text": match_print_text[2]})

    # Print variable
    match_print_var = re.match(r'(print|say) (\w+)', line, re.IGNORECASE)
    if match_print_var:
        return ParsedCommand("print_var", {"var": match_print_var[2]})

    # If x is greater than 10, print "..."
    match_if = re.match(r'if (\w+) is greater than (\d+), print "(.*)"', line, re.IGNORECASE)
    if match_if:
        return ParsedCommand("if_print", {
            "var": match_if[1],
            "value": int(match_if[2]),
            "text": match_if[3]
        })

    # Repeat 3 times: print "Hello"
    match_repeat = re.match(r'repeat (\d+) times: print "(.*)"', line, re.IGNORECASE)
    if match_repeat:
        return ParsedCommand("repeat_print", {
            "count": int(match_repeat[1]),
            "text": match_repeat[2]
        })

    # Unknown
    return ParsedCommand("unknown", {"raw": line})
