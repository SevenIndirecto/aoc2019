#!/usr/bin/env python3

# Advent of code Year 2019 Day 10 solution
# Author = seven
# Date = December 2019
import math
from io import StringIO

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()

space = []

space_width = None
y = 0

for line in StringIO(input):
    space_width = len(line)
    row = []

    for x in range(space_width):
        char = line[x]
        if char == '#':
            row.append(x)

    y += 1
    space.append(row)


def print_space():
    for row in space:
        row_str = ''

        for x in range(space_width):
            row_str += '#' if x in row else '.'

        print(row_str)


def map_hash(x1, y1, x2, y2):
    if x1 < x2 or (x1 == x2 and y1 < y2):
        xl = x1
        xh = x2
        yl = y1
        yh = y2
    else:
        xl = x2
        xh = x1
        yl = y2
        yh = y1

    return yl + xl * 100 + yh * 100 * 100 + xh * 100 * 100 * 100


location_detect_num = []

# True if points can see each other
can_pairs_see_eachother = {}

def log(msg: str):
    print(msg)
    pass

# Only check the rect area between (x1,y1) and (x2,y2)
def is_los_blocked(x1, y1, x2, y2):
    # log('--------------------')
    # log('LOS Check [{}, {}] - [{}, {}]'.format(x1, y1, x2, y2))
    # log('--------------------')
    y_min = min(y1, y2)
    y_max = max(y1, y2)
    x_min = min(x1, x2)
    x_max = max(x1, x2)

    # Special case if x2 == x1
    if x2 == x1:
        for y_between in range(y_min + 1, y_max):
            if x1 in space[y_between]:
                # LoS blocked
                # log('X1=X2 LoS Block [{}, {}] - [{}, {}] - [{}, {}]'.format(x1, y1, x1, y_between, x2, y2))
                return True
        # log('No block due to no points between ({}, {}) for x={}'.format(y_min + 1, y_max, x1))
        return False

    k = (y2 - y1) / (x2 - x1)
    n = y2 - k * x2

    for y_between in range(y_min, y_max + 1):
        for x_between in space[y_between]:
            if x_between < x_min or (x_between == x1 and y_between == y1) or (x_between == x2 and y_between == y2):
                # log('Continue [{}, {}] - [{}, {}] - [{}, {}]'.format(x1, y1, x_between, y_between, x2, y2))
                continue

            if x_between > x_max:
                # log('Break [{}, {}] - [{}, {}] - [{}, {}]'.format(x1, y1, x_between, y_between, x2, y2))
                break

            calc = abs(k * x_between + n - y_between)
            if calc >= 0 and calc < 1e-8:
                # log('Calc [{}, {}] - [{}, {}] - [{}, {}] k:{} n:{} calc:{}'.format(x1, y1, x_between, y_between, x2, y2, k, n, calc))
                # log('Block detected [{}, {}] - [{}, {}] - [{}, {}]'.format(x1, y1, x_between, y_between, x2, y2))
                # Detected a line of sight block
                return True

    # log('No LOS block detected [{}, {}] - [{}, {}]'.format(x1, y1, x2, y2))
    return False


def get_asteroids_in_sight_of(x1, y1, space, can_pairs_see_eachother):
    can_see_num = []

    for y2 in range(len(space)):
        for x2 in space[y2]:
            if y1 == y2 and x1 == x2:
                continue

            # Already visited these pairs
            key = map_hash(x1, y1, x2, y2)
            if key in can_pairs_see_eachother:
                # log('Pair already visited [{}, {}] - [{}, {}]'.format(x1, y1, x2, y2))

                if can_pairs_see_eachother[key]:
                    can_see_num.append((x2, y2))

                continue

            # Check for all points between
            blocked = is_los_blocked(x1, y1, x2, y2)

            if not blocked:
                can_see_num.append((x2, y2))

            can_pairs_see_eachother[map_hash(x1, y1, x2, y2)] = not blocked

    return can_see_num


for y1 in range(len(space)):
    for x1 in space[y1]:
        can_see = get_asteroids_in_sight_of(x1, y1, space, can_pairs_see_eachother)
        location_detect_num.append((x1, y1, len(can_see), can_see))


best = None
for asteroid in location_detect_num:
    if best is None or asteroid[2] > best[2]:
        best = asteroid



for y in range(len(space)):
    row_str = ''
    row = space[y]

    for x in range(space_width):
        if x == best[0] and y == best[1]:
            row_str += ' O'

        elif (x, y) in best[3]:
            row_str += ' *'

        else:
            row_str += ' #' if x in row else '  '

    print(row_str)


# print(best)
print("Part One : " + str(best[2]))

# START Part Two
print('Checking from point [{}, {}]'.format(best[0], best[1]))

settings = {
    'STEP': 0.001,
    'VERTICAL_SLOPE': 60,
    'DECIMALS': 3
}
quadrants = [
    {'start': 60.1, 'end': 0, 'in_quadrant': lambda x, y: x >= 0 and y >= 0},
    {'start': 0.1, 'end': -60, 'in_quadrant': lambda x, y: x >= 0 and y < 0},
    {'start': 60.1, 'end': 0, 'in_quadrant': lambda x, y: x < 0 and y <= 0},
    {'start': 0.1, 'end': -60, 'in_quadrant': lambda x, y: x < 0 and y > 0},
]

shots = {}


def scan_quadrant(quadrant, settings, shots, gun):
    # Translate coordinate system and make our Gun (xg, yg) the center (0, 0)

    xg, yg, _, asteroids_in_los = gun
    kg = quadrant['start']

    while kg > quadrant['end']:
        kg = round(kg - settings['STEP'], settings['DECIMALS'])

        closest = None

        for x_orig, y_orig in asteroids_in_los:
            # Translate to [xg, yg] as center
            x = x_orig - xg
            y = yg - y_orig

            if not quadrant['in_quadrant'](x, y):
                continue

            dist = None
            if x == 0:
                if abs(kg) >= settings['VERTICAL_SLOPE']:
                    dist = abs(y)
            else:
                k = y / x
                if abs(kg - k) < settings['STEP']:
                    # Possible hit
                    dist = math.sqrt(x**2 + y**2)

            if dist is not None:
                if closest is None or dist < closest[1]:
                    closest = ((x_orig, y_orig), dist)

        if closest is not None:
            # mark hit
            key = '{},{}'.format(closest[0][0], closest[0][1])
            if key not in shots:
                shots[key] = {
                    'ast': (closest[0][0], closest[0][1]), 'shot_num': len(shots) + 1, 'slope': kg
                }


while True:
    for q in quadrants:
        scan_quadrant(q, settings, shots, best)

    if len(shots) >= 200:
        break

    # After a full scan, clear destroyed
    for shot in shots.values():
        x, y = shot['ast']

        if x in space[y]:
            space[y].remove(x)

    # Now find new asteroids in sight
    can_see = get_asteroids_in_sight_of(best[0], best[1], space, {})
    best = (best[0], best[1], len(can_see), can_see)

    if len(best[3]) < 1:
        break

# print(shots)
number200 = next(filter(lambda el: el['shot_num'] == 200, shots.values()))
print(number200)
print('Part Two: {}'.format(100 * int(number200['ast'][0]) + int(number200['ast'][1])))

