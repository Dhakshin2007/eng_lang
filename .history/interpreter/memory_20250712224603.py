# interpreter/memory.py

class Memory:
    def __init__(self):
        self.variables = {}

    def set(self, name, value):
        self.variables[name] = value

    def get(self, name):
        return self.variables.get(name, None)

    def exists(self, name):
        return name in self.variables
