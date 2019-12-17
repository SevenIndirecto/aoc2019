#!/usr/bin/env python3

# Advent of code Year 2019 Day 13 solution
# Author = seven
# Date = December 2019

import enum
import random
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm
import curses
from curses import wrapper

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class Move(enum.Enum):
    north = 1
    south = 2
    west = 3
    east = 4


class Tile(enum.Enum):
    wall = 0
    normal = 1
    oxygen = 2


class Droid(vm.VM):
    def __init__(self, program: str):
        self.locations = {}
        self.pos = (0, 0)
        self.last_attempted_move = None

        self.locations[self.grid_key(self.pos)] = {
            'type': Tile.normal,
            'moves': 0,
            'pos': self.pos
        }
        self.oxygen_key = None

        # self.stdscr = stdscr

        super().__init__(program=program, input=MoveInput(droid=self), output=vm.IO())

    @staticmethod
    def get_loc_based_on_move(current_pos: tuple, move: Move):
        if move == Move.north:
            return (current_pos[0], current_pos[1] + 1)
        elif move == Move.south:
            return (current_pos[0], current_pos[1] - 1)
        elif move == Move.west:
            return (current_pos[0] - 1, current_pos[1])
        elif move == Move.east:
            return (current_pos[0] + 1, current_pos[1])
        raise ValueError('Invalid Move {}'.format(move))

    def load_from_input(self, a: vm.Param):
        super().load_from_input(a)
        self.last_attempted_move = Move(self.input.value)

    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)

        pos_key = self.grid_key(self.pos)
        next_pos = self.get_loc_based_on_move(self.pos, self.last_attempted_move)
        next_pos_key = self.grid_key(next_pos)
        moves = self.locations[pos_key]['moves'] + 1

        if next_pos_key in self.locations and self.locations[next_pos_key]['moves'] < moves:
            moves = self.locations[next_pos_key]['moves']

        if self.output.value == 0:
            self.locations[next_pos_key] = {'type': Tile.wall, 'moves': None, 'pos': next_pos}
        elif self.output.value == 1:
            self.pos = next_pos
            self.locations[next_pos_key] = {'type': Tile.normal, 'moves': moves, 'pos': next_pos}
        else:
            self.pos = next_pos
            self.locations[next_pos_key] = {'type': Tile.oxygen, 'moves': moves, 'pos': next_pos}
            self.oxygen_key = next_pos_key

    @staticmethod
    def grid_key(pos: tuple):
        x, y = pos
        return '{},{}'.format(x, y)

    def num_of_type(self, tile_type: Tile):
        count = 0
        for loc_meta in self.locations.values():
            if loc_meta['type'] == tile_type:
                count += 1
        return count

    def paint_state(self):
        print('----------------------------------------')
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for location in self.locations.values():
            x, y = location['pos']
            max_x = x if max_x is None else max(max_x, x)
            min_x = x if min_x is None else min(min_x, x)
            max_y = y if max_y is None else max(max_y, y)
            min_y = y if min_y is None else min(min_y, y)

        tile_to_str = ['#', '.', 'O']

        for y in range(min_y, max_y + 1):
            line = ''

            for x in range(min_x, max_x + 1):
                key = self.grid_key((x, y))
                if (x, y) == self.pos:
                    line += 'D'
                elif key in self.locations:
                    line += tile_to_str[self.locations[key]['type'].value]
                else:
                    line += ' '

            print(line)


class MoveInput(vm.IO):
    def __init__(self, droid: Droid):
        self.droid = droid
        super().__init__()

    @vm.IO.value.getter
    def value(self):
        x, y = self.droid.pos


        # Find first unexplored position and go there
        if self.droid.grid_key((x, y+1)) not in self.droid.locations:
            return Move.north.value
        elif self.droid.grid_key((x, y-1)) not in self.droid.locations:
            return Move.south.value
        elif self.droid.grid_key((x+1, y)) not in self.droid.locations:
            return Move.east.value
        elif self.droid.grid_key((x-1, y)) not in self.droid.locations:
            return Move.west.value

        # Else all have been explored, take path with least movement
        # even if it means moving back
        candidates = []
        variants = [
            (0, 1, Move.north.value),
            (0, -1, Move.south.value),
            (1, 0, Move.east.value),
            (-1, 0, Move.west.value)
        ]
        moves_to_here = self.droid.locations[self.droid.grid_key(self.droid.pos)]['moves']

        for dx, dy, direction in variants:
            pos = (x + dx, y + dy)
            key = self.droid.grid_key(pos)

            if key not in self.droid.locations:
                continue

            if self.droid.locations[key]['type'] == Tile.wall:
                continue

            moves = self.droid.locations[key]['moves']
            if moves_to_here > moves:
                if len(candidates) < 1 or candidates[0]['moves'] == moves:
                    candidates.append({'moves': moves, 'direction': direction})
                elif candidates[0]['moves'] > moves:
                    candidates = []
                    candidates.append({'moves': moves, 'direction': direction})

        if len(candidates) < 1:
            # No more moves left, stop the program
            self.droid.is_suspended = True
            return Move.north.value

        selected_candidate = random.choice(candidates)
        return selected_candidate['direction']


droid = Droid(program=input)
droid.run()
droid.paint_state()

print('Part One: {0}'.format(droid.locations[droid.oxygen_key]['moves']))

oxy_areas = set()
oxy_areas.add(droid.oxygen_key)

min_x = None
max_x = None
min_y = None
max_y = None

for location in droid.locations.values():
    x, y = location['pos']
    max_x = x if max_x is None else max(max_x, x)
    min_x = x if min_x is None else min(min_x, x)
    max_y = y if max_y is None else max(max_y, y)
    min_y = y if min_y is None else min(min_y, y)

minute = 0
adjecant = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]

while droid.num_of_type(Tile.normal) > 0:
    newly_oxadized = set()

    for o_key in oxy_areas:
        x, y = droid.locations[o_key]['pos']
        for dx, dy in adjecant:
            key = droid.grid_key((x + dx, y + dy))
            if key not in droid.locations:
                continue

            if droid.locations[key]['type'] == Tile.normal:
                newly_oxadized.add(key)
                droid.locations[key]['type'] = Tile.oxygen

    oxy_areas = newly_oxadized
    minute += 1

droid.paint_state()
print('Part two: {}'.format(minute))
