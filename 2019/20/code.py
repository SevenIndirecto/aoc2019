#!/usr/bin/env python3

# Advent of code Year 2019 Day 20 solution
# Author = seven
# Date = December 2019

import enum
from collections import deque
from io import StringIO

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class Tile(enum.Enum):
    empty = 0
    wall = 1
    entrance = 2
    exit = 3
    portal = 4
    none = 5


class Portal(enum.Enum):
    inner = 0
    outer = 1


portals = {}
entrance = None
exit = None

num_lines = input.count('\n') + 1
line_length = len(input[0:input.find('\n')])
maze = []
portal_grid = []
for _ in range(num_lines):
    maze.append([None] * line_length)
    portal_grid.append([None] * line_length)

y = 0
for line in StringIO(input):
    row = []
    for x in range(line_length):
        if line[x] == ' ':
            maze[y][x] = (Tile.none, ' ')
            continue
        elif line[x] == '.':
            maze[y][x] = (Tile.empty, '.')
        elif line[x] == '#':
            maze[y][x] = (Tile.wall, '#')
        else:
            maze[y][x] = (Tile.none, line[x])
            portal_grid[y][x] = line[x]

    y += 1

unpaired_portals = {}
for y in range(len(portal_grid)):
    for x in range(len(portal_grid[y])):
        if portal_grid[y][x] is None:
            continue

        portal_id = None
        # Vertical portal
        if y > 0 and portal_grid[y-1][x] is not None:
            portal_id = '{}{}'.format(portal_grid[y-1][x], portal_grid[y][x])

        # Horizontal portal
        elif x > 0 and portal_grid[y][x-1] is not None:
            portal_id = '{}{}'.format(portal_grid[y][x-1], portal_grid[y][x])

        if portal_id is not None:
            candidates = [(0,-2), (0, 1), (-2, 0), (1, 0)]
            for dx, dy in candidates:
                px = x + dx
                py = y + dy

                if py >= len(portal_grid) or px >= len(portal_grid[py]) or maze[py][px][0] is not Tile.empty:
                    continue

                if portal_id == 'AA':
                    entrance = (px, py)
                    maze[py][px] = (Tile.entrance, '^')
                elif portal_id == 'ZZ':
                    exit = (px, py)
                    maze[py][px] = (Tile.exit, '$')
                else:
                    maze[py][px] = (Tile.portal, portal_id)
                    is_outer_portal = x == 1 or x == line_length - 1 or y == 1 or y == num_lines - 1
                    portal_type = Portal.outer if is_outer_portal else Portal.inner

                    if portal_id in unpaired_portals:
                        portals[(px, py)] = (unpaired_portals[portal_id][0], portal_type, portal_id)
                        portals[unpaired_portals[portal_id][0]] = ((px, py), unpaired_portals[portal_id][1], portal_id)
                        unpaired_portals.pop(portal_id)
                    else:
                        unpaired_portals[portal_id] = ((px, py), portal_type)

for y in range(len(maze)):
    line = ''
    for x in range(len(maze[y])):
        if maze[y][x][0] is Tile.portal:
            line += 'I' if portals[(x, y)][1] is Portal.inner else 'O'
        else:
            line += maze[y][x][1][0:1]
    print(line)


def find_shortest_path(maze, portals, entrance, exit):
    discovered = {}
    q = deque()

    discovered[entrance] = 0
    q.append((entrance[0], entrance[1], 0))

    while len(q) > 0:
        x, y, distance = q.popleft()
        pos = (x, y)

        if maze[y][x][0] is Tile.exit:
            return distance

        # Use portal
        if maze[y][x][0] is Tile.portal:
            # print('Use portal {} from {} to {}'.format(portals[pos][2], pos, portals[pos][0]))
            pos = portals[pos][0]
            x, y = pos
            distance += 1
            discovered[pos] = distance

        candidates = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in candidates:
            ax = x + dx
            ay = y + dy
            adj_pos = (ax, ay)

            if maze[ay][ax][0] not in [Tile.empty, Tile.exit, Tile.portal]:
                continue

            if adj_pos not in discovered or discovered[adj_pos] > distance:
                discovered[adj_pos] = distance + 1
                q.append((ax, ay, distance + 1))


distance = find_shortest_path(maze, portals, entrance, exit)
print("Part One : " + str(distance))


def find_shortest_path_recursive_maze(maze, portals, entrance, exit):
    discovered = {}
    q = deque()

    discovered[(entrance[0], entrance[1], 0)] = 0
    q.append((entrance[0], entrance[1], 0, 0))

    while len(q) > 0:
        x, y, distance, depth = q.popleft()
        pos = (x, y)
        # print('Check {} distance {} depth {}'.format(pos, distance, depth))

        if maze[y][x][0] is Tile.exit and depth == 0:
            return distance

        # Use portal
        if maze[y][x][0] is Tile.portal and (depth > 0 or portals[pos][1] is Portal.inner):
            portal_new_pos, portal_type, _ = portals[pos]

            depth_before = depth
            if portal_type is Portal.inner:
                depth += 1
            else:
                depth -= 1

            # print('Use portal {} ({}) from {} to {} distance {} depth: {} -> {}'.format(
                # portals[pos][2], portals[pos][1], pos, portals[pos][0], distance+1, depth_before, depth
            # ))
            x, y = portal_new_pos
            distance += 1
            discovered[(x, y, depth)] = distance

        candidates = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in candidates:
            ax = x + dx
            ay = y + dy
            adj_key = (ax, ay, depth)

            if maze[ay][ax][0] is Tile.exit and not depth == 0:
                continue

            if maze[ay][ax][0] not in [Tile.empty, Tile.exit, Tile.portal]:
                continue

            if adj_key not in discovered or discovered[adj_key] > distance:
                if depth < 1 and maze[ay][ax][0] is Tile.portal and portals[(ax, ay)][1] is Portal.outer:
                    continue

                discovered[(ax, ay, depth)] = distance + 1
                q.append((ax, ay, distance + 1, depth))

print('Processing part Two...')
distance_recursive_maze = find_shortest_path_recursive_maze(maze, portals, entrance, exit)
print("Part Two : " + str(distance_recursive_maze))
