#!/usr/bin/env python3

# Advent of code Year 2019 Day 24 solution
# Author = seven
# Date = December 2019

from io import StringIO

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()

eris = {0: []}
size = 5


def load_level0(input: str):
    level0 = []
    for line in StringIO(input):
        row = []
        for c in line.strip():
            row.append(1 if c == '#' else 0)
        level0.append(row)
    return level0


def draw_eris():
    for level in sorted(eris.keys()):
        print('Depth {}'.format(level))
        draw_level(level)
        print('')


def draw_level(level):
    print()
    line = ''
    for y in range(len(eris[level])):
        line = ''
        for x in range(len(eris[level][y])):
            if x == size // 2 and y == size // 2:
                line += '?'
            else:
                line += '#' if eris[level][y][x] == 1 else '.'
        print(line)


def level_to_mask(level):
    i = 0
    mask = 0
    for y in range(len(eris[level])):
        for x in range(len(eris[level][y])):
            if eris[level][y][x] == 1:
                mask |= 2**i
            i += 1
    return mask


eris[0] = load_level0(input)
prev_eris_mask = level_to_mask(0)
eris_mask_history = set()
neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]

draw_level(0)
while prev_eris_mask not in eris_mask_history:
    new_eris = [[0] * size for _ in range(size)]
    # tick
    for y in range(size):
        for x in range(size):
            bugs = 0
            for dx, dy in neighbors:
                nx = x + dx
                ny = y + dy

                if ny < 0 or nx < 0 or ny >= size or nx >= size:
                    continue

                bugs += eris[0][ny][nx]

            is_current_bug = eris[0][y][x] == 1
            new_eris[y][x] = (
                1 if (is_current_bug and bugs == 1) or (not is_current_bug and (bugs == 1 or bugs == 2)) else 0
            )

    eris_mask_history.add(prev_eris_mask)
    eris[0] = new_eris
    prev_eris_mask = level_to_mask(0)
    draw_level(0)


print("Part One : " + str(prev_eris_mask))

eris = {
    -1: [[0] * size for _ in range(size)],
    0: [],
    1: [[0] * size for _ in range(size)]
}
eris[0] = load_level0(input)

mid = size // 2

draw_eris()
minutes = 200
for tick in range(minutes):
    new_eris_layout = {}
    for level in eris.keys():
        new_level_layout = [[0] * size for _ in range(size)]

        for y in range(size):
            for x in range(size):
                if x == mid and y == mid:
                    continue

                adj_bugs = 0
                for dx, dy in neighbors:
                    nx = x + dx
                    ny = y + dy

                    # adjecant tile is on inner level
                    if nx == mid and ny == mid:
                        if level+1 not in new_eris_layout:
                            new_eris_layout[level+1] = [[0] * size for _ in range(size)]

                        if level+1 not in eris:
                            continue

                        if dx == 1:
                            adj_bugs += sum([l[0] for l in eris[level+1]])
                        elif dx == -1:
                            adj_bugs += sum([l[size-1] for l in eris[level+1]])
                        elif dy == -1:
                            adj_bugs += sum(eris[level+1][size-1])
                        else:
                            adj_bugs += sum(eris[level+1][0])

                    # adjecant tile is on outer level
                    elif nx == -1 or nx == size or ny == -1 or ny == size:
                        if level-1 not in new_eris_layout:
                            new_eris_layout[level-1] = [[0] * size for _ in range(size)]

                        if level-1 not in eris:
                            continue

                        if nx == -1:
                            adj_bugs += eris[level-1][mid][mid-1]
                        elif nx == size:
                            adj_bugs += eris[level-1][mid][mid+1]
                        elif ny == -1:
                            adj_bugs += eris[level-1][mid-1][mid]
                        else:
                            adj_bugs += eris[level-1][mid+1][mid]

                    # adjecant tile is on same level
                    else:
                        adj_bugs += eris[level][ny][nx]

                is_current_bug = eris[level][y][x] == 1
                new_level_layout[y][x] = (
                    1 if (is_current_bug and adj_bugs == 1) or (not is_current_bug and (adj_bugs == 1 or adj_bugs == 2)) else 0
                )

        new_eris_layout[level] = new_level_layout

    eris = new_eris_layout

draw_eris()

bugs = 0
for level in eris.values():
    for row in level:
        bugs += sum(row)

print('Bugs on Eris after {} minutes => {}'.format(minutes, bugs))

