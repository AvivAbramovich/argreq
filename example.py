from argreq import argument, requirement
from argreq.errors import NotMetRequirementError, ArgumentNotFoundError
import functools

def return_true(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if res is None:
            return True
    return wrapper

@return_true
@argument('a', '>10', type=int)
def int_grater_than_10(a):
    print(f'a ({a}) is int and larger then 10!')

@return_true
@argument('a', ('>10', '<20'), type=int)
def int_between_10_to_20(a):
    print(f'a {a} is int and between 10 and 20')

@return_true
@argument('d', '"a" in {}')
def dict_with_a(d):
    print(f'd ({d}) has "a" in it')

@argument('a', '1/{}')
def power_minus_one(a):
    '''Requirements might raise exceptions'''
    print('requirement should raise')

@return_true
@requirement('{a}>0 and {b}>0')
def only_positives(**kwargs):
    print(f'{kwargs} are positives!')

if __name__ == '__main__':
    assert int_grater_than_10(11)
    assert int_grater_than_10(200)
    assert int_between_10_to_20(15)
    assert dict_with_a({'a': 0})
    assert only_positives(a=1,b=2)

    try:
        int_grater_than_10(8)
        int_grater_than_10(7.0)
        dict_with_a({})
        only_positives(a=1,b=-3)
        func_with_req(a=1)
        power_minus_one(0)
    except:
        pass
