
argreq
======

Add requirements to function arguments using simple and elegant decorators

Installation:
-------------

.. code-block:: bash

   pip install argreq

Examples
--------

.. code-block:: python

   from argreq import argument

   @argument('a', '>10', type=int)
   def int_grater_than_10(a):
       '''If a is smaller than 10, function raises 'NotValidArgumentError' '''
       print(f'a ({a}) is int and larger then 10!')

   @argument('a', ('>10', '<20'), type=int)
   def other_func(a):
       '''Check if a is grater than 10 AND smaller than 20'''
       print(f'a {a} is int and between 10 and 20')

   @argument('a', '10<{}<20', type=int)
   def prettier_other_func(a):
       '''Same as above but in a single requirement'''
       print(f'a ({a}) is int and between 10 and 20 and prettier ;)')

   @argument('a','>0')
   @argument('b','>0')
   def div(a,b):
       '''Check if both a and b positive'''
       print(f'{a}/{b}={a/b}')

   @argument('d', '"a" in {}', type=dict)
   def dict_func(d):
       '''Check if d has the key 'a' '''
       print(f'd ({d}) has "a" in it')
