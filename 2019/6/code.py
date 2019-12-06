# Advent of code Year 2019 Day 6 solution
# Author = seven
# Date = December 2019
import io

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class SpaceBall(object):
    def __init__(self, id: str, center: str, indirect_orbits: int):
        self.id = id
        self.center = center
        self.indirect_orbits = indirect_orbits
        self.directly_orbited_by = set()
        self.visited = False

    def __repr__(self):
        return '[{0}: {1} - {2}]'.format(self.id, self.indirect_orbits, self.directly_orbited_by)

    def add_ball_to_orbit(self, ball_id: str):
        self.directly_orbited_by.add(ball_id)

keys_orbiting_values = {}

for orbit in io.StringIO(input):
    center_ball, orbiting_ball = tuple(orbit.strip().split(')'))
    keys_orbiting_values[orbiting_ball] = center_ball

space_map = {
    'COM': SpaceBall('COM', None, -1)
}


def add_ball(ball: str, center: str):

    if not ball in space_map and not center in space_map:
        add_ball(center, keys_orbiting_values[center])

    if ball in space_map:
        return

    if center in space_map:
        # add ball
        center_balls_indirect_orbits = space_map[center].indirect_orbits
        space_map[ball] = SpaceBall(id=ball, center=center, indirect_orbits=center_balls_indirect_orbits + 1)
        space_map[center].add_ball_to_orbit(ball)
        return


for orbiting_ball, center_ball in keys_orbiting_values.items():
    add_ball(orbiting_ball, center_ball)


def calc_total_orbits():
    total_orbits = sum([ball.indirect_orbits + 1 for ball in space_map.values()])
    return total_orbits

print("Part One : " + str(calc_total_orbits()))


path_to_santa_length = 0
path_found = False


def find_path_to_santa(ball: SpaceBall, path_length: int):
    global path_found
    global path_to_santa_length

    if path_found or ball.visited:
        return

    ball.visited = True

    if 'SAN' in ball.directly_orbited_by:
        # found SANTA
        path_to_santa_length = path_length + 1
        path_found = True
        return

    for orbiting_ball_id in ball.directly_orbited_by:
        find_path_to_santa(space_map[orbiting_ball_id], path_length + 1)

    if not path_found:
        find_path_to_santa(space_map[ball.center], path_length + 1)


find_path_to_santa(space_map['YOU'], 0)

print("Part Two : " + str(path_to_santa_length - 2))
