#!/usr/bin/env python3

# Advent of code Year 2019 Day 13 solution
# Author = seven
# Date = December 2019

import enum
import re
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class Dir(enum.Enum):
    up = 0
    right = 1
    down = 2
    left = 3


class Tile(enum.Enum):
    robot = 0
    scaffold = 35
    empty = 46


class Ascii(vm.VM):
    def __init__(self, program: str, movement: str = ''):
        self.map = {}
        self.pos = (0, 0)
        self.max_x = None
        self.min_x = None
        self.max_y = None
        self.min_y = None
        self.robot = {}

        self.movement = movement
        self.movement_out_pos = 0
        super().__init__(program=program, input=vm.IO(), output=vm.IO())

    def load_from_input(self, a: vm.Param):
        char = self.movement[self.movement_out_pos]
        self.input.value = ord(char)
        self.movement_out_pos += 1
        super().load_from_input(a)

    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)

        out = self.output.value
        if out == 10:
            # newline
            self.pos = (0, self.pos[1] + 1)
            return

        self.max_x = self.pos[0] if self.max_x is None else max(self.max_x, self.pos[0])
        self.min_x = self.pos[0] if self.min_x is None else min(self.min_x, self.pos[0])
        self.max_y = self.pos[1] if self.max_y is None else max(self.max_y, self.pos[1])
        self.min_y = self.pos[1] if self.min_y is None else min(self.min_y, self.pos[1])

        if out == Tile.scaffold.value or out == Tile.empty.value:
            self.map[str(self.pos)] = Tile(out)
        else:
            # robot
            if out == 60:
                robot_dir = Dir.left
            elif out == 62:
                robot_dir = Dir.right
            elif out == 94:
                robot_dir = Dir.up
            else:
                robot_dir = Dir.down
            self.map[str(self.pos)] = Tile.robot
            self.robot = {
                'x': self.pos[0],
                'y': self.pos[1],
                'dir': robot_dir
            }

        self.pos = (self.pos[0] + 1, self.pos[1])

    def paint_state(self):
        for y in range(self.min_y, self.max_y + 1):
            line = ''
            for x in range(self.min_x, self.max_x + 1):
                key = str((x, y))
                if self.map[key] == Tile.robot:
                    if self.robot['dir'] == Dir.up:
                        line += '^'
                    elif self.robot['dir'] == Dir.down:
                        line += 'v'
                    elif self.robot['dir'] == Dir.left:
                        line += '<'
                    else:
                        line += '>'
                else:
                    line += chr(self.map[key].value)

            print(line)

    def alignment_sum(self):
        checksum = 0

        for y in range(self.min_y, self.max_y):
            for x in range(self.min_x, self.max_x):
                key = str((x, y))
                if not self.map[key] == Tile.scaffold:
                    continue

                if y-1 < self.min_y or y+1 > self.max_y or x+1 > self.max_x or x-1 < self.min_x:
                    continue

                above = str((x, y-1))
                right = str((x+1, y))
                below = str((x, y+1))
                left = str((x-1, y))

                if (
                    self.map[above] == Tile.scaffold and self.map[right] == Tile.scaffold and
                    self.map[below] == Tile.scaffold and self.map[left] == Tile.scaffold
                ):
                    checksum += x * y
        return checksum

    def get_traversal_string(self):
        path = ''

        while True:
            # Rotate to unvisited area
            # Try to rotate left
            rotation = 'L'
            self.rotate_robot(-1)
            next_area_in_dir = self.get_next_move_area_in_current_dir()

            if next_area_in_dir is None:
                # Try rotating right instead
                self.rotate_robot(1)
                self.rotate_robot(1)
                rotation = 'R'
                next_area_in_dir = self.get_next_move_area_in_current_dir()

            if next_area_in_dir is None:
                # Neither left not right are possible areas, so end reached
                break

            path += rotation

            # Move max amount possible in current direction
            count = 0
            while next_area_in_dir is not None:
                self.robot['x'] = next_area_in_dir[0]
                self.robot['y'] = next_area_in_dir[1]

                next_area_in_dir = self.get_next_move_area_in_current_dir()
                count += 1

            path += str(count)

        return path

    def get_next_move_area_in_current_dir(self):
        dx = 0
        dy = 0
        if self.robot['dir'] == Dir.left:
            dx = -1
        elif self.robot['dir'] == Dir.right:
            dx = 1
        elif self.robot['dir'] == Dir.up:
            dy = -1
        else:
            dy = 1

        x = self.robot['x'] + dx
        y = self.robot['y'] + dy
        key = str((x, y))

        if not self.is_valid_area(x, y) or not self.map[key] == Tile.scaffold:
            return None

        return (x, y)

    def is_valid_area(self, x, y):
        return y >= self.min_y and y <= self.max_y and x <= self.max_x and x >= self.min_x

    def rotate_robot(self, direction: int):
        if self.robot['dir'] == Dir.up and direction == -1:
            self.robot['dir'] = Dir.left
        else:
            self.robot['dir'] = Dir((self.robot['dir'].value + direction) % 4)


program = Ascii(program=input)
program.run()
program.paint_state()

print('Part One: {0}'.format(program.alignment_sum()))

# Determine path
path = program.get_traversal_string()
print(path)


def create_movement_func(path, depth, used_patterns):
    replacement_char = 'x'

    if depth > 3:
        were_valid_patterns_used = path.replace(replacement_char, '') == ''
        return (were_valid_patterns_used, used_patterns)

    for pattern_length in range(2, 12):
        offset = 0

        while offset < len(path) - pattern_length:
            pattern = path[offset:offset+pattern_length]

            if replacement_char in pattern:
                offset += 1
                continue

            new_path = path.replace(pattern, replacement_char)

            history = '{},{}'.format(used_patterns, pattern)

            found, full_history = create_movement_func(new_path, depth+1, history)

            if found:
                return (True, full_history)

            offset += 1
    return (False, '')


result = create_movement_func(path, 1, '')
patterns = result[1][1:].split(',')

out = path
replacers = ['A', 'B', 'C']
for i in range(len(patterns)):
    out = out.replace(patterns[i], replacers[i])

movement_logic = '{}\n'.format(','.join([c for c in out]))
replacer = re.compile(r'(\d+)')

for p in patterns:
    rep = replacer.sub(r',\1,', p)[0:-1]
    movement_logic += '{}\n'.format(rep)

movement_logic += 'n\n'
print(movement_logic)

part2 = Ascii(program=input, movement=movement_logic)
part2.memory.set(addr=0, value=2)
part2.run()

print('Part two: {}'.format(part2.output.value))
