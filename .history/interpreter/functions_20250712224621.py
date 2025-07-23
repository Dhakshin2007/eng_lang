# interpreter/functions.py

class FunctionManager:
    def __init__(self):
        self.functions = {}

    def define(self, name, body_lines):
        self.functions[name.lower()] = body_lines

    def get(self, name):
        return self.functions.get(name.lower(), None)

    def exists(self, name):
        return name.lower() in self.functions
