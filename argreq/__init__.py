from  typing import Callable, Union, Tuple, List, Dict, Any
import inspect
import functools
import builtins
import functools
import re

import argreq.errors

__VERSION__ = '0.2.0'

VAR_NAMES_NON_EMPTY_PATTERN = re.compile(r'({([a-zA-Z_$][a-zA-Z_$0-9]*)})')
VAR_NAMES_AND_EMPTY_PATTERN = re.compile(r'({([a-zA-Z_$][a-zA-Z_$0-9]*)?})')

def _find_argument(
    func : Callable, 
    arg_name : str, 
    args : List, 
    kwargs : Dict[str, Any]
):
    if arg_name in kwargs:
        return kwargs[arg_name]
    else:
        func_args = inspect.getfullargspec(func).args
        if arg_name in func_args:
            return args[func_args.index(arg_name)]
        raise argreq.errors.ArgumentNotFoundError(arg_name)

def _check_requirement(name : str, value, req : Union[str, Tuple[str]], type=None):
    if type is not None:
        if not isinstance(value, type):
            raise TypeError(type(value))
    def check(_req):
        search_res = VAR_NAMES_AND_EMPTY_PATTERN.findall(_req)
        if not search_res:
            expression = f'value{_req}'
        else:
            format_args = []
            format_kwargs = {}
            for _, arg_name in search_res:
                if arg_name == '':
                    format_args.append(value)
                elif arg_name == name:
                    format_kwargs[name] = value
                else:
                    raise argreq.errors.InvalidArgumentError(name, arg_name, _req)
            expression = _req.format(*format_args, **format_kwargs)            
        if not eval(expression):
            raise argreq.errors.NotMetRequirementError(_req, expression)
    if builtins.type(req) in [tuple, list]:
        for _req in req:
            check(_req)
    else:
        check(req)


def argument(
    name : str, 
    req : Union[str, Tuple[str], List[str]], 
    type = None,
    required : bool = False
):
    '''
    Add requirements for specific variable
    :param name: str. the name of the argument
    :param req: the requirement(s). It can be in multiple form.
        1. Simple form - not including the variable but only a simple expression like ">10". In this case, the function adds the variable in front of the expression and then eavluate it.
        2. Using empty or named {} - for example: "{}>10", "10<{}<20", "3 in {var_name}" etc.
        3. List or Tuple of any of the above form. In this case, all the requirements are tested and raising if any of them fails.

        If any requirement not met, raising `argreq.errors.NotMetRequirementError`
    :param type: cls, Optional. A specific type of the argument. Raising `TypeError` if not match.
    :param required: bool, Optional. If the argument is required. If set to false and argument not given, raising `argreq.errors.ArgumentNotFoundError`
    
    :returns: None
    
    :raises: `TypeError`, `argreq.errors.NotMetRequirementError`, `argreq.errors.ArgumentNotFoundError`, `argreq.errors.InvalidArgumentError`
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                value = _find_argument(func, name, args, kwargs)
            except argreq.errors.ArgumentNotFoundError as e:
                if required:
                    raise e
            else:
                _check_requirement(name, value, req, type)

            return func(*args, **kwargs)
        return wrapper
    return decorator

def requirement(
    expression : str,
    required : bool = True
):
    '''Test a general requirement for function argument(s)
    :param expression: a valid python expression using `{arg_name}` to specify the function arguments to test, for example: `{a}>{b}`,`{item} in {a}.values()`, etc.
    :param required: bool, Optional. If set to true and one the arguments mentioned in the expression is missing, raising `argreq.errors.ArgumentNotFoundError`.
    
    :raises: `argreq.errors.NotMetRequirementError`, `argreq.errors.ArgumentNotFoundError`
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            search_res = VAR_NAMES_NON_EMPTY_PATTERN.findall(expression)
            format_kwargs = {}
            should_eval = True
            for _, arg_name in search_res:
                try:
                    format_kwargs[arg_name] = _find_argument(func, arg_name, args, kwargs)
                except argreq.errors.ArgumentNotFoundError as e:
                    if required:
                        raise e
                    else:
                        should_eval = False
                        break
            if should_eval:
                _exp = expression.format(**format_kwargs)
                if not eval(_exp):
                    raise argreq.errors.NotMetRequirementError(requirement, _exp)
            return func(*args, **kwargs)
        return wrapper
    return decorator
