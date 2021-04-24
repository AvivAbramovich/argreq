from  typing import Callable, Union, Tuple, List, Dict, Any
import inspect
import functools
import builtins
import functools

import argreq.errors

__VERSION__ = '0.1.0'


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
        if '{}' in _req:
            req_with_arg = _req.format(value)
        elif f'{{name}}' in _req:
            req_with_arg = _req.format(**{name: value})
        else:
            req_with_arg = f'value{_req}'
        if not eval(req_with_arg):
            raise NotValidArgumentError(value, _req)
    if builtins.type(req) is tuple:
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
