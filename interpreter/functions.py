# interpreter/functions.py

class FunctionManager:
    def __init__(self):
        self.functions = {}

    def define(self, name, body, param=None):
        self.functions[name] = {
            "body": body,
            "param": param
        }

    def get(self, name):
        return self.functions.get(name)

    def get(self, name):
        return self.functions.get(name.lower(), None)

    def exists(self, name):
        return name.lower() in self.functions
