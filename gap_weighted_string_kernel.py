#!/usr/bin/env python
# -*- coding: utf-8 -*-

def indices(t, x):
    ret = [];
    pos = -1;
    while True:
        pos = t.find(x, pos + 1)
        if pos != -1:
            ret.append(pos)
        else:
            break
    return ret


def K(i, s, t, l):
    if min(len(s), len(t)) < i:
        return 0

    return K(i, s[0:-1], t, l) + l ** 2 * sum([K1(i - 1, s[0:-1], t[0:j], l) for j in indices(t, s[-1])])


def K1(i, s, t, l):
    if i == 0:
        return 1

    if min(len(s), len(t)) < i:
        return 0

    return l * K1(i, s[0:-1], t, l) + K2(i, s, t, l)


def K2(i, s, t, l):
    if min(len(s), len(t)) < i:
        return 0

    if s[-1] == t[-1]:
        return l * (K2(i, s, t[0:-1], l) + l * K1(i -1, s[0:-1], t[0:-1], l))
    else:
        return l * K2(i, s, t[0:-1], l)



# sample code
import sys

s = 'nokuno'
t = 'tokyonlp'

# for Japanese
s = unicode(s, 'utf-8')
t = unicode(t, 'utf-8')

print K(2, s, t, 0.7)
