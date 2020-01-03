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


class Springdroid(vm.VM):
    def __init__(self, program: str, script: str = ''):
        self.script = script
        self.script_read_pos = 0
        self.ascii_out = ''
        super().__init__(program=program, input=vm.IO(), output=vm.IO())

    def load_from_input(self, a: vm.Param):
        char = self.script[self.script_read_pos]
        self.input.value = ord(char)
        self.script_read_pos += 1
        super().load_from_input(a)

    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)
        if self.output.value < 256:
            char_code = self.output.value
            self.ascii_out += chr(char_code)

# Condition -> Optimized with negations applied where it leads to less instructions
# (!A or !B or !C) and D -> !(A and B and C) and D
script = """
OR A J
AND B J
AND C J
NOT J J
AND D J
WALK
""".lstrip()

program = Springdroid(program=input, script=script)
program.run()
print(program.ascii_out)

print('Part 1: {}'.format(program.output.value))

# Condition -> Optimized with negations applied where it leads to less instructions
# (!A or !B or !C) and D and !(!E and !H) -> !(A and B and C) and D and (E or H)
script2 = """
OR A J
AND B J
AND C J
NOT J J
AND D J
OR E T
OR H T
AND T J
RUN
""".lstrip()
program = Springdroid(program=input, script=script2)
program.run()
print(program.ascii_out)

print('Part 2: {}'.format(program.output.value))
