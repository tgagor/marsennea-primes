#!/usr/bin/env python

import random
from multiprocessing import Pool, cpu_count
# from multiprocessing.pool import ThreadPool
from functools import cache, lru_cache

Sbuf = {}


# @lru_cache(maxsize=100)
@cache
def S(k, N):
    # return 4 if k == 1 else S(k-1)**2-2
    return 4 if k == 1 else (S(k-1, N)**2-2) % N


@cache
def test_lucasa_lehmera(p):
    """
    Testujemy czy 2^p-1 jest pierwsza

    Test Lucasa-Lehmera wymaga nieparzystego p > 1
    """
    # if p%2 != 0 and p > 1:
    # martwe sprawdzenie - przy obecnych zalozeniach nigdy nie wypadnie
    N = 2**p-1
    for k in range(1, p):
        # if S(k) % N == 0:
        if S(k, N) % N == 0:
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


def check_if_prime(exponent):
    # LM wymagaja pierwszego p
    if test_rabina(exponent):
        # if test_rabina(2**i-1): # sprawdzamy czy nie bedzie szybciej :)
        if(test_lucasa_lehmera(exponent)):
            res = "LM: 2^%d-1 = %d" % (exponent, 2**exponent-1)
            print(res)


if __name__ == '__main__':
    MAX_EXPONENT = 5000
    exponents = range(3, MAX_EXPONENT, 2)

    with Pool(cpu_count()) as p:
        p.map(check_if_prime, exponents)
