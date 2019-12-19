#!/usr/bin/env python3

# Advent of code Year 2019 Day 16 solution
# Author = seven
# Date = December 2019
import time
from functools import reduce

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


def phase(lin: list):
    size = len(lin)
    lout = [0] * size

    for depth in range(size):
        period = (depth + 1) * 4
        plus_offset = depth

        plus_sum = 0
        i = plus_offset
        while i < size:
            plus_sum += sum(lin[i:i+depth+1])
            i += period

        minus_offset = depth + period // 2
        minus_sum = 0
        i = minus_offset
        while i < size:
            minus_sum += sum(lin[i:i+depth+1])
            i += period

        lout[depth] = abs(plus_sum - minus_sum) % 10

    return lout


base_pattern = [0, 1, 0, -1]
lout = [int(c) for c in input.rstrip()]

for i in range(100):
    lout = phase(lout)

part_one = ''.join([str(c) for c in lout[0:8]])
print("Part One : " + str(part_one))

# Part two note:
# ... figured this out only after significant hints / solutions.
# Can being sick at the time  be blamed?
# Nah I'm just dumb, but at least I can
# monkey actualize the code ¯\_(ツ)_/¯


# The 8 digit message we're looking for is in the 2nd half of the pattern
offset = int(input[0:7])
lin = [int(c) for c in input.rstrip()] * 10000
# The property of these transformation is that for the second half of the list
# each element is just a sum of all the preceededing elements starting from the
# end of the list (mod 10 of course).

loff = lin[offset:]
loff_len = len(loff)

print('Offset {}, length: {}'.format(offset, loff_len))

for _ in range(100):
    loff_new = [loff[-1]] * loff_len

    for i in range(loff_len - 2, -1, -1):
        loff_new[i] = abs(loff_new[i+1] + loff[i]) % 10

    loff = loff_new

part2 = ''.join(str(d) for d in loff[0:8])
print("Part Two : " + part2)

