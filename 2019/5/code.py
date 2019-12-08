#!/usr/bin/env python3

# Advent of code Year 2019 Day 2 solution
# Author = seven
# Date = December 2019

import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()

try:
    proc1 = vm.VM(program=input, input=vm.IO(initial=1), output=vm.IO())
    proc1.run()
    print('Part one: {0}'.format(proc1.output.value))
except ValueError as e:
    print(e)

try:
    proc2 = vm.VM(program=input, input=vm.IO(initial=5), output=vm.IO())
    proc2.run()
    print('Part two: {0}'.format(proc2.output.value))
except Exception as e:
    print(e)
