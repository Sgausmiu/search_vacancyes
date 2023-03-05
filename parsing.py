import sympy
from sympy import *

def is_prime(number) -> bool:
    return sympy.isprime(number)


print(is_prime(11))


