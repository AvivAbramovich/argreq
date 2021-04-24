class NotMetRequirementError(Exception):
    def __init__(self, requirement, expression):
        self.requirement = requirement
        self.expression = expression
    def __str__(self):
        return f'Rquirement "{self.requirement}" not met'

class ArgumentNotFoundError(Exception):
    def __init__(self, arg_name):
        self.arg_name = arg_name
    def __str__(self):
        return f'Argument {arg_name} not found'

class InvalidArgumentError(Exception):
    def __init__(self, orig_name, arg_name, requirement):
        self.orig_argument = orig_name
        self.arg_name = arg_name
        self.requirement = requirement
    def __str__(self):
        return f'"{self.orig_argument}" Argument requirement contains other argument name ("{self.arg_name}")'