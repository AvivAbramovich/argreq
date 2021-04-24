
class NotValidArgumentError(Exception):
    def __init__(self, value, requirement):
        self.value = value
        self.requirement = requirement
    
    def __str__(self):
        return f'The value {{value}} not fulfill requirement "{requirement}"'

class ArgumentNotFoundError(Exception):
    def __init__(self, arg_name):
        self.arg_name = arg_name
    def __str__(self):
        return f'Argument {arg_name} not found'
