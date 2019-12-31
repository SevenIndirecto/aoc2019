#!/usr/bin/env python3

# Advent of code Year 2019 Day 13 solution
# Author = seven
# Date = December 2019

import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class AnalyzePoint(vm.VM):
    def __init__(self, program: str, drone_pos: tuple):
        self.drone_pos = drone_pos
        self.input_mode = 0

        super().__init__(program=program, input=vm.IO(), output=vm.IO())

    def load_from_input(self, a: vm.Param):
        self.input.value = self.drone_pos[self.input_mode]
        self.input_mode = (self.input_mode+1) % 2
        super().load_from_input(a)


def paint_state(tractor_beam, min_x, max_x, min_y, max_y, square_pos, square_size):
    for y in range(min_y, max_y + 1):
        line = ''
        for x in range(min_x, max_x + 1):
            if x >= square_pos[0] and x < square_pos[0] + square_size and y >= square_pos[1] and y < square_pos[1] + square_size:
                line += '0'
            else:
                line += '#' if (x, y) in tractor_beam else '.'
        print(line)


tractor_beam = set()
max_x = 49
max_y = 15000
square_size = 100

x_low_bound = 0
x_high_bound = max_x
x_high_bound_calibrated = False

highest_x = -1
highest_y = -1
square_pos = None

tracted_in_50_50 = None

# These high / low bounds could be kept tighter to speed up, but kept it loose...
for y in range(max_y + 1):
    highest_y = y
    if square_pos is not None:
        break

    if tracted_in_50_50 is None and y >= 50:
        tracted_in_50_50 = len(tractor_beam)

    print('Check range {} to {} for y: {}'.format(x_low_bound, x_high_bound, y))

    is_first_in_line_found = False
    for x in range(x_low_bound, x_high_bound + 1):
        if is_first_in_line_found and x <= highest_x:
            tractor_beam.add((x, y))
        else:
            program = AnalyzePoint(program=input, drone_pos=(x, y))
            program.run()

            if program.output.value == 0:
                continue

            is_first_in_line_found = True

            if not x_high_bound_calibrated and not (0, 0) == (x, y):
                highest_x = x
                x_high_bound = x + 2
                x_high_bound_calibrated = True

            if x > 0 and (x-1, y) not in tractor_beam:
                x_low_bound = x
            if x >= x_high_bound:
                x_high_bound += 2

            if x > highest_x:
                highest_x = x

            tractor_beam.add((x, y))

        # At this point we've added a tracted position, check if square fits
        if x - x_low_bound >= square_size - 1:
            top_right = (x, y - square_size + 1)
            if top_right in tractor_beam:
                square_pos = (x_low_bound, y - square_size + 1)
                break

print('Part One: {0}'.format(tracted_in_50_50))

x, y = square_pos
print('Part Two: {}'.format(x * 10**4 + y))
print(square_pos)

