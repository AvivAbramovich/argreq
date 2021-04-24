from argreq import argument, NotValidArgumentError
import functools
import pytest

def return_true(func):
    functools.wraps(func)
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

def test_argument():
    assert int_grater_than_10(11)
    assert int_grater_than_10(200)
    assert int_between_10_to_20(15)
    assert dict_with_a({'a': 0})

    with pytest.raises(NotValidArgumentError):
        int_grater_than_10(8)
    with pytest.raises(TypeError):
        int_grater_than_10(7.0)
    with pytest.raises(NotValidArgumentError):
        dict_with_a({})
