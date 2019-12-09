#!/usr/bin/env python3

# Advent of code Year 2019 Day 9 solution
# Author = seven
# Date = December 2019

import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()

class PrintOnOutput(vm.VM):
    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)
        print('OUTPUT: {0}'.format(self.get_param_value(a)))

boost = PrintOnOutput(program=input, input=vm.IO(initial=1), output=vm.IO())
boost.run()

print('Part One: {0}'.format(boost.output.value))

boost = PrintOnOutput(program=input, input=vm.IO(initial=2), output=vm.IO())
boost.run()
print('Part Two: {0}'.format(boost.output.value))

