#!/usr/bin/env python3

# Advent of code Year 2019 Day 9 solution
# Author = seven
# Date = December 2019

import enum
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class Ship(object):
    def __init__(self):
        self.panels = {}

    def panelAt(self, pos: tuple):
        pos = str(pos)

        if pos in self.panels:
            return self.panels[pos]
        return {'color': 0}

    def paintPanel(self, pos: tuple, color: int):
        pos_str = str(pos)

        if pos not in self.panels:
            self.panels[pos_str] = {'color': 0, 'visited': 0, 'x': pos[0], 'y': pos[1]}

        # print('Paint {} {} ({})'.format(pos, 'Black' if color == 0 else 'White', color))
        self.panels[pos_str]['color'] = color
        self.panels[pos_str]['visited'] += 1


class Dir(enum.Enum):
    up = 0
    right = 1
    down = 2
    left = 3


class Robot(vm.VM):
    def __init__(self, program: str, ship: Ship):
        self.ship = ship
        self.position = (0, 0)
        self.direction = Dir.up
        self.waiting_to_paint = True
        super().__init__(program=program, input=vm.IO(), output=vm.IO())

    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)

        if self.waiting_to_paint:
            self.ship.paintPanel(self.position, self.output.value)
            self.waiting_to_paint = False
        else:
            self.turn(self.output.value)
            self.move()
            self.waiting_to_paint = True

    def load_from_input(self, a: vm.Param):
        self.input.value = self.ship.panelAt(self.position)['color']
        super().load_from_input(a)

    def turn(self, direction: int):
        delta = 1 if direction == 1 else -1
        dir_str = 'Turn from {}'.format(self.direction)
        if self.direction == Dir.up and delta == -1:
            self.direction = Dir.left
        else:
            self.direction = Dir((self.direction.value + delta) % 4)

        # print('{} to {} (Command: {})'.format(dir_str, self.direction, direction))

    def move(self):
        mov_str = 'Move from {}'.format(self.position)

        if self.direction == Dir.up:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.direction == Dir.right:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.direction == Dir.down:
            self.position = (self.position[0], self.position[1] - 1)
        else:
            self.position = (self.position[0] - 1, self.position[1])

        # print('{} to {} direction: {}'.format(mov_str, self.position, self.direction))


ship = Ship()
robot = Robot(program=input, ship=ship)
robot.run()


print('Part One: {0}'.format(len(ship.panels)))

ship = Ship()
ship.panels[str((0, 0))] = {'color': 1, 'visited': 0, 'x': 0, 'y': 0}
robot = Robot(program=input, ship=ship)
robot.run()

print('Part two')

min_x = None
max_x = None
min_y = None
max_y = None

for panel in ship.panels.values():
    min_x = panel['x'] if min_x is None else min(panel['x'], min_x)
    max_x = panel['x'] if max_x is None else max(panel['x'], max_x)
    min_y = panel['y'] if min_y is None else min(panel['y'], min_y)
    max_y = panel['y'] if max_y is None else max(panel['y'], max_y)

for y in range(max_y, min_y - 1, -1):
    line = ''
    for x in range(min_x, max_x + 1):
        pos = str((x, y))
        if pos in ship.panels and ship.panels[pos]['color'] == 1:
            line += '|'
        else:
            line += ' '
    print(line)
