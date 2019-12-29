#!/usr/bin/env python3

# Advent of code Year 2019 Day 18 solution
# Author = seven
# Date = December 2019
import copy
import enum
import re
from collections import deque
from io import StringIO


class Tile(enum.Enum):
    empty = 0
    wall = 1
    key = 2
    door = 3
    entrance = 4


def print_maze(maze):
    for y in range(len(maze)):
        line = ''
        for x in range(len(maze[y])):
            line += maze[y][x][1]
        print(line)


def load_maze_grid(maze_str: str):
    maze = []
    droids = {}
    graph_nodes = []
    match_key = r'[a-z]'
    match_door = r'[A-Z]'

    y = 0
    for row_str in StringIO(input):
        row = []
        x = 0
        for c in row_str.rstrip():
            if c == '@':
                graph_nodes.append((x, y))
                droid_id = str(len(droids) + 1)
                row.append((Tile.entrance, droid_id))
                droids[droid_id] = droid_id
            elif c == '.':
                row.append((Tile.empty, c))
            else:
                if re.match(match_key, c):
                    row.append((Tile.key, c))
                    graph_nodes.append((x, y))
                elif re.match(match_door, c):
                    row.append((Tile.door, c))
                    graph_nodes.append((x, y))
                else:
                    row.append((Tile.wall, '#'))
            x += 1

        maze.append(row)
        y += 1

    return (maze, droids, graph_nodes)


def maze_grid_to_graph(maze, graph_nodes):
    # Determine edges for all graph nodes using BFS
    maze_graph = {}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    all_key_mask = 0

    for pos in graph_nodes:
        discovered = {}
        discovered[pos] = 0
        edges = []
        q = deque()
        q.append((pos[0], pos[1], 0))

        while len(q) > 0:
            x, y, steps = q.popleft()
            tile_type, tile_repr = maze[y][x]

            for dx, dy in directions:
                ax = x + dx
                ay = y + dy
                adj = (ax, ay)

                if ay >= len(maze) or ax >= len(maze[ay]) or ax < 0 or ay < 0:
                    # out of bounds
                    continue

                if adj not in discovered:
                    discovered[adj] = steps + 1
                    adj_type, adj_repr = maze[ay][ax]

                    if adj_type is Tile.key or adj_type is Tile.door:
                        edges.append((adj_repr, steps + 1))
                    elif adj_type is Tile.empty or adj_type is Tile.entrance:
                        q.append((ax, ay, steps + 1))

        tile_type, tile_repr = maze[pos[1]][pos[0]]

        maze_graph[tile_repr] = {
            'edges': edges,
            'type': tile_type,
            'mask': 0,
        }

        if tile_type is Tile.key or tile_type is Tile.door:
            power = ord(tile_repr.lower()) - ord('a')
            key_mask = 2**power
            all_key_mask |= key_mask
            maze_graph[tile_repr]['mask'] = key_mask

    return (maze_graph, all_key_mask)


def least_steps_to_collect_all_keys(maze: dict, droids_initial: list, all_key_mask: int):
    """
    Args:
        maze: graph of keys, doors and starting point. Each node is a dict
            node = id: {'edges': list[(key_id, dist)], 'type': Tile, 'mask': int}
        start: starting key id
    """
    q = deque()
    discovered = {}

    discovered[(droids_initial['1'], 0)] = 0
    q.append((droids_initial['1'], 0, 0, '1', droids_initial))

    lowest_steps = None
    while len(q) > 0:
        node_id, steps, collected_keys_mask, active_droid_id, droids = q.popleft()
        droids[active_droid_id] = node_id

        if maze[node_id]['type'] is Tile.key:
            collected_keys_mask |= maze[node_id]['mask']

        if collected_keys_mask == all_key_mask:
            if lowest_steps is None or steps < lowest_steps:
                lowest_steps = steps

        for droid_id, droid_pos in droids.items():
            for edge_id, edge_dist in maze[droid_pos]['edges']:
                key = (edge_id, collected_keys_mask)

                if key not in discovered or steps + edge_dist < discovered[key]:
                    n = maze[edge_id]

                    if n['type'] is Tile.door and n['mask'] & collected_keys_mask == 0:
                        # Encountered closed doors
                        continue

                    # Either open door, key or start
                    discovered[key] = steps + edge_dist
                    q.append((edge_id, steps + edge_dist, collected_keys_mask, droid_id, copy.deepcopy(droids)))

    return lowest_steps


# Part 1
with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()

maze_grid, droids, graph_nodes = load_maze_grid(input)
maze_graph, all_key_mask = maze_grid_to_graph(maze_grid, graph_nodes)
min_steps = least_steps_to_collect_all_keys(maze_graph, droids, all_key_mask)
print('Part 1: {} steps'.format(min_steps))


# Part 2
with open((__file__.rstrip("code.py") + "input2.txt"), 'r') as input_file:
    input = input_file.read()

maze_grid, droids, graph_nodes = load_maze_grid(input)
maze_graph, all_key_mask = maze_grid_to_graph(maze_grid, graph_nodes)
min_steps = least_steps_to_collect_all_keys(maze_graph, droids, all_key_mask)
print('Part 2: {} steps'.format(min_steps))

