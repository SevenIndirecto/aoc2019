#!/usr/bin/env python3

# Advent of code Year 2019 Day 4 solution
# Author = seven
# Date = December 2019

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()

start, end = tuple([int(i) for i in input.split('-')])


def int_to_list(num):
    return [int(d) for d in str(num)]


def list_to_int(num_as_list):
    return int(''.join(map(str, num_as_list)))


hits = []
n = int_to_list(start)
pos = 0

while True:
    # check if end hit
    as_int = list_to_int(n)

    if as_int > end:
        break

    # check if valid
    prev = n[0]
    is_increasing = True
    has_double = False

    for digit in range(1, 6):
        if n[digit] == prev:
            has_double = True
        if n[digit] < prev:
            is_increasing = False
            break
        prev = n[digit]

    if is_increasing and has_double:
        hits.append(as_int)

    # find pos to increase
    if all([9 == digit_to_right for digit_to_right in n[pos:]]):
        # increase self and set all to the right to self
        n[pos] += 1
        for right_digit_pos in n[pos:]:
            n[right_digit_pos] = n[pos]
    else:
        as_int += 1
        n = int_to_list(as_int)


print("Part One : " + str(len(hits)))

filtered_hit_num = 0

# Remove larger groups of matching digits
for num_as_int in hits:
    n = int_to_list(num_as_int)

    count = 1
    has_valid_double = False
    valid_double = None

    prev = n[0]
    for digit in range(1, 6):
        if n[digit] == prev:
            if has_valid_double:
                if valid_double == n[digit]:
                    has_valid_double = False
                    count += 1
                else:
                    count = 1

            elif count < 2 or not valid_double == n[digit]:
                has_valid_double = True
                valid_double = n[digit]
                count = 2

        prev = n[digit]

    if has_valid_double:
        filtered_hit_num += 1


print("Part Two : " + str(filtered_hit_num))

