from argreq import argument
from argreq.errors import NotValidArgumentError
import functools

def return_true(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if res is None:
            return True
        return res    
    return wrapper


@return_true
@argument('a', '>10', type=int, required=True)
def myfunc(a):
    print(f'a ({a}) is int and larger then 10!')

@return_true
@argument('a', ('>10', '<20'), type=int)
def other_func(a):
    print(f'a {a} is int and between 10 and 20')

@return_true
@argument('a', '10<{}<20', type=int)
def prettier_other_func(a):
    print(f'a ({a}) is int and between 10 and 20 and prettier ;)')

@return_true
@argument('a','>0')
@argument('b','>0')
def div(a,b):
    print(f'{a}/{b}={a/b}')

@return_true
@argument('d', '"a" in {}')
def dict_func(d):
    print(f'd ({d}) has "a" in it')

if __name__ == '__main__':
    assert myfunc(11)
    assert myfunc(200)
    assert other_func(15)
    assert prettier_other_func(15)
    assert div(1,2)
    assert dict_func({'a': 0})

    #myfunc(8)
    #myfunc(7.0)
    #dict_func({})