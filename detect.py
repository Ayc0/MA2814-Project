# -*- coding: utf8 -*-

letters = set()

with open('input.txt', 'r') as f:
    for line in f.readlines():
        for char in line:
            letters.add(char)

a = list(letters)
a.sort()

print(''.join(a))