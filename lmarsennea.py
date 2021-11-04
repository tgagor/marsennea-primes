#!/usr/bin/env python

import random

Sbuf = {}


def S(k, N):
    if(k not in Sbuf):
        Sbuf[k] = 4 if k == 1 else (S(k-1, N)**2-2) % N

    return Sbuf[k]


def test_lucasa_lehmera(p):
    # if p%2 != 0 and p > 1:
    # martwe sprawdzenie - przy obecnych zalozeniach nigdy nie wypadnie
    for k in range(1, p):
        # print("S(%d) = %d" % (k,w))
        N = 2**p-1
        if S(k, N) % N == 0:
            return True
    return False


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


if __name__ == '__main__':
    for i in range(3, 4450):
        Sbuf = {}

        # LM wymagaja pierwszego p
        if test_rabina(i):
            # if test_rabina(2**i-1): # sprawdzamy czy nie bedzie szybciej :)
            if(test_lucasa_lehmera(i)):
                res = "LM: 2^%d-1=%d -> " % (i, 2**i-1)
                print(res + "jest pierwsza")
