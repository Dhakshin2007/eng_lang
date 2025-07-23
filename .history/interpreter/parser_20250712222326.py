# interpreter/parser.py

import re

class ParsedCommand:
    def __init__(self, action, args):
        self.action = action
        self.args = args

def parse_command(line):
    line = line.strip()

    if line.startswith("Let"):
    # Case 1: Let x be 5
        match_number = re.match(r"Let (\w+) be (\d+)", line)
        if match_number:
            return ParsedCommand("assign", {
                "var": match_number[1],
            "value": int(match_number[2])
        })

    # Case 2: Let name be "Dhakshin"
    match_string = re.match(r'Let (\w+) be "(.*)"', line)
    if match_string:
        return ParsedCommand("assign", {
            "var": match_string[1],
            "value": match_string[2]
        })


    elif line.startswith("Add"):
        match = re.match(r"Add (\d+) to (\w+)", line)
        if match:
            return ParsedCommand("add", {"value": int(match[1]), "var": match[2]})

    elif line.startswith("Print") or line.startswith("Say"):
        # Print "something"
        match = re.match(r'(Print|Say) "(.*)"', line)
        if match:
            return ParsedCommand("print_text", {"text": match[2]})
        
        # Print variable
        match_var = re.match(r'(Print|Say) (\w+)', line)
        if match_var:
            return ParsedCommand("print_var", {"var": match_var[2]})


    elif line.startswith("If"):
        match = re.match(r"If (\w+) is greater than (\d+), print \"(.*)\"", line)
        if match:
            return ParsedCommand("if_print", {
                "var": match[1], "value": int(match[2]), "text": match[3]
            })

    elif line.startswith("Repeat"):
        match = re.match(r"Repeat (\d+) times: print \"(.*)\"", line)
        if match:
            return ParsedCommand("repeat_print", {
                "count": int(match[1]), "text": match[2]
            })

    return ParsedCommand("unknown", {"raw": line})
