from argreq import argument, requirement
from argreq.errors import NotMetRequirementError, ArgumentNotFoundError
import functools
import pytest

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
@argument('a', ['>10', '<20'], type=int)
def int_between_10_to_20_list(a):
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

@return_true
@requirement('{a}>{b}>0')
def a_grater_than_b_and_positives(a, b):
    print(f'{a} > {b}')

def test_argument():
    assert int_grater_than_10(11)
    assert int_grater_than_10(200)
    assert int_between_10_to_20(15)
    assert int_between_10_to_20_list(15)
    assert dict_with_a({'a': 0})
    assert only_positives(a=1,b=2)
    assert a_grater_than_b_and_positives(5,3)

    with pytest.raises(NotMetRequirementError):
        int_grater_than_10(8)
    with pytest.raises(TypeError):
        int_grater_than_10(7.0)
    with pytest.raises(NotMetRequirementError):
        dict_with_a({})
    with pytest.raises(NotMetRequirementError):
        int_between_10_to_20_list(1)
    with pytest.raises(NotMetRequirementError):
        only_positives(a=1,b=-3)
    with pytest.raises(ArgumentNotFoundError):
        only_positives(a=1)
    with pytest.raises(ZeroDivisionError):
        power_minus_one(0)
    with pytest.raises(NotMetRequirementError):
        a_grater_than_b_and_positives(3,6)
    with pytest.raises(NotMetRequirementError):
        a_grater_than_b_and_positives(3,-1)
