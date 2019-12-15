#!/usr/bin/env python3

# Advent of code Year 2019 Day 13 solution
# Author = seven
# Date = December 2019

import enum
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm
import curses
from curses import wrapper

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class Tile(enum.Enum):
    empty = 0
    wall = 1
    block = 2
    paddle = 3
    ball = 4


class ReadMode(enum.Enum):
    x = 0
    y = 1
    tile_id = 2


class Game(vm.VM):
    def __init__(self, program: str, stdscr=None):
        self.grid = {}
        self.output_count = 0
        self.tile_pos = [None, None]
        self.max_x = None
        self.min_x = None
        self.max_y = None
        self.min_y = None

        self.stdscr = stdscr
        self.ball = None
        self.paddle = None
        self.score = None

        super().__init__(program=program, input=Joystick(game=self), output=vm.IO())

    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)

        mode = ReadMode(self.output_count % 3)

        if ReadMode.x == mode:
            self.tile_pos[0] = self.output.value
        elif ReadMode.y == mode:
            self.tile_pos[1] = self.output.value
        else:
            if self.tile_pos[0] == -1 and self.tile_pos[1] == 0:
                self.score = self.output.value
                self.output_count += 1
                return

            self.max_x = self.tile_pos[0] if self.max_x is None else max(self.max_x, self.tile_pos[0])
            self.min_x = self.tile_pos[0] if self.min_x is None else min(self.min_x, self.tile_pos[0])
            self.max_y = self.tile_pos[1] if self.max_y is None else max(self.max_y, self.tile_pos[1])
            self.min_y = self.tile_pos[1] if self.min_y is None else min(self.min_y, self.tile_pos[1])

            tile = Tile(self.output.value)
            self.grid[self.grid_key(self.tile_pos[0], self.tile_pos[1])] = tile

            if tile == Tile.ball:
                self.ball = [self.tile_pos[0], self.tile_pos[1]]
            elif tile == Tile.paddle:
                self.paddle = [self.tile_pos[0], self.tile_pos[1]]
                if self.stdscr is not None:
                    self.paint_curses()

        self.output_count += 1

    @staticmethod
    def grid_key(x: int, y: int):
        return '{},{}'.format(x, y)

    def paint_curses(self):
        tile_to_str = [' ', '#', '*', '_', 'O']

        for y in range(self.min_y, self.max_y + 1):
            line = ''

            for x in range(self.min_x, self.max_x + 1):
                key = self.grid_key(x, y)
                if key in self.grid:
                    line += tile_to_str[self.grid[key].value]
                else:
                    line += '?'

            self.stdscr.addstr(y, 0, line)
        self.stdscr.addstr(self.max_y + 1, 0, 'Score: {}'.format(self.score))
        self.stdscr.refresh()

    def paint_state(self):
        tile_to_str = [' ', '#', '*', '_', 'O']

        for y in range(self.min_y, self.max_y + 1):
            line = ''

            for x in range(self.min_x, self.max_x + 1):
                key = self.grid_key(x, y)
                if key in self.grid:
                    line += tile_to_str[self.grid[key].value]
                else:
                    line += '?'

            print(line)
        print('Score: {}'.format(self.score))

    def get_num_of_type(self, tile_id: Tile):
        count = 0
        for tile in self.grid.values():
            if tile == tile_id:
                count += 1
        return count


class Joystick(vm.IO):
    def __init__(self, game: Game):
        self.game = game
        super().__init__()

    @vm.IO.value.getter
    def value(self):
        if self.game.ball[0] < self.game.paddle[0]:
            return -1
        elif self.game.ball[0] > self.game.paddle[0]:
            return 1
        return 0


game = Game(program=input)
game.run()
game.paint_state()

print('Part One: {0}'.format(game.get_num_of_type(Tile.block)))


def part_two(stdscr, score):
    stdscr.clear()
    game = Game(program=input, stdscr=stdscr)
    game.memory.set(addr=0, value=2)
    game.run()
    score.append(game.score)


score = []
game = wrapper(part_two, score)
print('Part two: {}'.format(score[0]))
