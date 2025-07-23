# interpreter/parser.py

import re

class ParsedCommand:
    def __init__(self, action, args):
        self.action = action
        self.args = args

def parse_command(line):
    line = line.strip()

    # Let x be 5
    match_number = re.match(r"Let (\w+) be (\d+)", line)
    if match_number:
        return ParsedCommand("assign", {
            "var": match_number[1],
            "value": int(match_number[2])
        })

    # Let name be "Dhakshin"
    match_string = re.match(r'Let (\w+) be "(.*)"', line)
    if match_string:
        return ParsedCommand("assign", {
            "var": match_string[1],
            "value": match_string[2]
        })

    # Add 3 to x
    match_add = re.match(r"Add (\d+) to (\w+)", line)
    if match_add:
        return ParsedCommand("add", {
            "value": int(match_add[1]),
            "var": match_add[2]
        })

    # Print "something"
    match_print_text = re.match(r'(Print|Say) "(.*)"', line)
    if match_print_text:
        return ParsedCommand("print_text", {"text": match_print_text[2]})

    # Print variable
    match_print_var = re.match(r'(Print|Say) (\w+)', line)
    if match_print_var:
        return ParsedCommand("print_var", {"var": match_print_var[2]})

    # If x is greater than 10, print "Hello"
    match_if = re.match(r"If (\w+) is greater than (\d+), print \"(.*)\"", line)
    if match_if:
        return ParsedCommand("if_print", {
            "var": match_if[1],
            "value": int(match_if[2]),
            "text": match_if[3]
        })

    # Repeat 3 times: print "Hello"
    match_repeat = re.match(r"Repeat (\d+) times: print \"(.*)\"", line)
    if match_repeat:
        return ParsedCommand("repeat_print", {
            "count": int(match_repeat[1]),
            "text": match_repeat[2]
        })

    return ParsedCommand("unknown", {"raw": line})
