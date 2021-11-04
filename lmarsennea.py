#!/usr/bin/env python

import random
from multiprocessing import Pool, cpu_count
# from multiprocessing.pool import ThreadPool
from functools import cache, lru_cache
import cProfile
from sympy.ntheory.primetest import mr
from dogpile.cache import make_region


region = make_region().configure(
    'dogpile.cache.dbm',
    expiration_time=300,
    arguments={
        "filename": "propable-primes.dbm"
    }
)


# it's counting only forward and require only one previous value actually
@lru_cache(maxsize=10)
def S(k, N):
    return 4 if k == 1 else (S(k-1, N)**2-2) % N


def test_lucasa_lehmera(p):
    """
    Testujemy czy 2^p-1 jest pierwsza

    Test Lucasa-Lehmera wymaga nieparzystego p > 1
    """
    # if p%2 != 0 and p > 1:
    # martwe sprawdzenie - przy obecnych zalozeniach nigdy nie wypadnie
    N = 2**p-1
    for k in range(1, p):
        if S(k, N) == 0:
            return True
    return False


@cache
def miller_rabin_pass(a, s, d, n):
    a_to_power = pow(a, d, n)
    if a_to_power == 1:
        return True
    for i in range(s-1):
        if a_to_power == n - 1:
            return True
        a_to_power = (a_to_power * a_to_power) % n
    return a_to_power == n - 1


@region.cache_on_arguments()
def test_rabina(n):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1

    for repeat in range(20):
        a = 0
        while a == 0:
            a = random.randrange(n)
        if not miller_rabin_pass(a, s, d, n):
            return False
    return True


def check_if_prime(p):
    # LM postaci 2**p-1 mogą być pierwsze tylko gdy p jest pierwsze
    # co nie jest jednak warunkiem dostatecznym

    # alternative to my test
    # https://www.johndcook.com/blog/2019/02/25/prime-test/
    # bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    # if mr(p, bases):

    # https://bigprimes.org/

    if test_rabina(p):
        # if test_rabina(2**p-1):  # sprawdzamy czy nie bedzie szybciej :)
        # PS: nie jest :)
        if(test_lucasa_lehmera(p)):
            N = 2**p-1
            print(f"LM: 2^{p}-1 = {N}")


def main():
    MAX_EXPONENT = 10000
    exponents = range(3, MAX_EXPONENT, 2)

    with Pool(cpu_count()) as p:
        p.map(check_if_prime, exponents)


if __name__ == '__main__':
    # cProfile.run('main()')
    main()
