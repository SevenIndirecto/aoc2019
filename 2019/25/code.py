#!/usr/bin/env python3

# Advent of code Year 2019 Day 25 solution
# Author = seven
# Date = December 2019

import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    program = input_file.read()


class Crawl(vm.VM):
    def __init__(self, program: str):
        self.input_buffer = ''
        self.input_buffer_read_pos = 0
        self.output_buffer = ''
        super().__init__(program=program, input=vm.IO(), output=vm.IO())

    def load_from_input(self, a: vm.Param):
        char = self.input_buffer[self.input_buffer_read_pos]
        self.input.value = ord(char)
        self.input_buffer_read_pos += 1
        super().load_from_input(a)

    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)
        if self.output.value < 256:
            char_code = self.output.value

            if char_code == 10:
                if self.output_buffer == 'Command?':
                    command = input('>')
                    self.input_buffer = command + '\n'
                    self.input_buffer_read_pos = 0
                else:
                    print(self.output_buffer)
                self.output_buffer = ''
            else:
                self.output_buffer += chr(char_code)


crawler = Crawl(program=program)
crawler.run()
