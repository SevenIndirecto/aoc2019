# Advent of code Year 2019 Day 3 solution
# Author = seven
# Date = December 2019

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class Line(object):
    def __init__(self, pa, pb, steps_start):
        self.pa = pa
        self.pb = pb
        self.is_vertical = pa[0] == pb[0]
        self.is_horizontal = not self.is_vertical
        self.steps_start = steps_start

    def __repr__(self):
        return '[' + str(self.pa) + ' ' + str(self.pb) + ']'

    def crossAt(self, line: 'Line'):
        cross = None

        if self.is_vertical and line.is_horizontal:
            cross = self._get_hor_and_ver_cross(line, self)
        elif self.is_horizontal and line.is_vertical:
            cross = self._get_hor_and_ver_cross(self, line)
        elif self.is_horizontal and line.is_horizontal:
            pass
        elif self.is_vertical and line.is_vertical:
            pass

        if cross is not None:
            steps = self.steps_start + man_dist(self.pa, cross)
            steps += line.steps_start + man_dist(line.pa, cross)
            return (cross, steps)

        return (None, None)

    @staticmethod
    def _get_hor_and_ver_cross(h, v):
        if (
            (
                (h.pa[0] <= v.pa[0] and v.pa[0] <= h.pb[0]) or (h.pb[0] <= v.pa[0] and v.pa[0] <= h.pa[0])
            )
            and
            (
                (v.pa[1] >= h.pa[1] and h.pa[1] >= v.pb[1]) or (v.pb[1] >= h.pa[1] and h.pa[1] >= v.pa[1])
            )
        ):
            return [v.pa[0], h.pa[1]]

        return None



def man_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def load_wire(path, wire):
    moves = path.split(',')

    curr_point = [0, 0]
    steps = 0

    for m in moves:
        direction = m[:1]

        coord = 0 if direction == 'R' or direction == 'L' else 1
        modifier = 1 if direction == 'R' or direction == 'U' else -1

        delta = int(m[1:])
        new_point = [curr_point[0], curr_point[1]]
        new_point[coord] += modifier * delta

        wire.append(Line(curr_point, new_point, steps))

        steps += delta
        curr_point = [new_point[0], new_point[1]]


wire1 = []
wire2 = []

paths = input.split('\n')
load_wire(paths[0], wire1)
load_wire(paths[1], wire2)

center = [0, 0]
best = None
best_dist = None
lowest_steps = None

# print(', '.join([str(w) for w in wire1]))
# print(', '.join([str(w) for w in wire2]))

for line1 in wire1:
    for line2 in wire2:
        cross, steps = line1.crossAt(line2)
        if cross is not None:
            dist = man_dist(center, cross)
            if dist <= 0:
                continue

            if lowest_steps is None or steps < lowest_steps:
                lowest_steps = steps

            if best_dist is None or dist < best_dist:
                best = cross
                best_dist = dist

print("Part One : " + str(best_dist))

print("Part Two : " + str(lowest_steps))
