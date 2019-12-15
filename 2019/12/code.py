#!/usr/bin/env python3

# Advent of code Year 2019 Day 12 solution
# Author = seven
# Date = December 2019

from io import StringIO
from math import gcd

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class Moon(object):
    def __init__(self, pos):
        self.pos = pos
        self.v = [0, 0, 0]

    def __repr__(self):
        return 'POS: {} V: {} P: {} K: {} T:{}'.format(
            self.pos, self.v, self.potential(), self.kinetic(), self.total_energy()
        )

    def potential(self):
        return sum([abs(dim) for dim in self.pos])

    def kinetic(self):
        return sum([abs(v) for v in self.v])

    def total_energy(self):
        return self.potential() * self.kinetic()


def applyGravity(moons):
    for m1 in range(0, len(moons)):
        for m2 in range(m1, len(moons)):
            for dim in range(3):
                if moons[m1].pos[dim] < moons[m2].pos[dim]:
                    moons[m1].v[dim] += 1
                    moons[m2].v[dim] -= 1
                elif moons[m1].pos[dim] > moons[m2].pos[dim]:
                    moons[m1].v[dim] -= 1
                    moons[m2].v[dim] += 1

def applyVelocity(moons):
    for moon in moons:
        for dim in range(3):
            moon.pos[dim] += moon.v[dim]

def load_moons(input: str):
    moons = []
    for line in StringIO(input):
        split = line.replace('>', '').replace('<', '').split(', ')
        pos = []
        for coord in split:
            pos.append(int(coord.split('=')[1]))
        moons.append(Moon(pos))
    return moons


moons = load_moons(input)
tick = 0

while tick < 1000:
    tick += 1
    applyGravity(moons)
    applyVelocity(moons)


def total_energy(moons):
    return sum([moon.total_energy() for moon in moons])


print("Part One : " + str(total_energy(moons)))

tick = 0
periods = [0, 0, 0]
periods_found = [False, False, False]

moons = load_moons(input)
istate = load_moons(input)

while not all(periods_found):
    tick += 1
    applyGravity(moons)
    applyVelocity(moons)

    for dim in range(3):
        if periods_found[dim]:
            continue

        is_period = True
        for i in range(len(moons)):
            if not istate[i].pos[dim] == moons[i].pos[dim] or not istate[i].v[dim] == moons[i].v[dim]:
                is_period = False
                break

        periods[dim] += 1

        if is_period:
            periods_found[dim] = True

print(periods)
print('Tick {}'.format(tick))


def lcm(a, b):
    return a * b / gcd(a, b)


print("Part Two : " + str(int(lcm(periods[0], int(lcm(periods[1], periods[2]))))))

