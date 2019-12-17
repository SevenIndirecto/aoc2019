#!/usr/bin/env python3

# Advent of code Year 2019 Day 14 solution
# Author = seven
# Date = December 2019

import math
from io import StringIO

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class NanoFactory(object):
    def __init__(self, input: str):
        self.chemicals = {}
        self.ore_used = 0

        for line in StringIO(input):
            line = line.rstrip('\n')
            split = line.split(' => ')
            amount, key = tuple(split[1].split(' '))
            self.chemicals[key] = {'amount_produced': int(amount), 'reaction': [], 'available': 0}

            reagents = split[0].split(', ')
            for r in reagents:
                r_amount, r_id = tuple(r.split(' '))
                self.chemicals[key]['reaction'].append({'amount': int(r_amount), 'id': r_id})

    def state(self):
        repr = ''
        for id, meta in self.chemicals.items():
            repr += '{},{}/'.format(id, meta['available'])
        return repr

    def build(self, id, amount):
        # print('BUILD {} {}'.format(amount, id))

        if amount <= self.chemicals[id]['available']:
            return True

        required = amount - self.chemicals[id]['available']
        build_times = math.ceil(required / self.chemicals[id]['amount_produced'])

        if self.chemicals[id]['reaction'][0]['id'] == 'ORE':
            created = build_times * self.chemicals[id]['amount_produced']
            self.chemicals[id]['available'] += created

            ore_used = build_times * self.chemicals[id]['reaction'][0]['amount']
            self.ore_used += ore_used
            # print('Used {} ore to produce {} {}'.format(ore_used, created, id))
            return True

        for reagent in self.chemicals[id]['reaction']:
            reagent_to_build = build_times * reagent['amount']

            self.build(reagent['id'], reagent_to_build)
            # print('Consumed {} {}'.format(reagent_to_build, reagent['id']))
            self.chemicals[reagent['id']]['available'] -= reagent_to_build

        self.chemicals[id]['available'] += build_times * self.chemicals[id]['amount_produced']



factory = NanoFactory(input=input)
factory.build('FUEL', 1)

print("Part One : " + str(factory.ore_used))

factory = NanoFactory(input=input)


ore_available = 1000000000000
##################################
# Find loops
##################################
# fuel_produced = 0
# prev_states = {}
# prev_states[factory.state()] = 0
# loop_found = False

# while factory.ore_used < ore_available:
#     factory.build('FUEL', 1)
#     factory.chemicals['FUEL']['available'] = 0

#     if factory.ore_used < ore_available:
#         fuel_produced += 1

#     if loop_found:
#         continue

#     key = factory.state()
#     if key in prev_states:
#         print('Found repeat {} at {} fuel produced'.format(prev_states[key], fuel_produced + 1))
#         times = ore_available // factory.ore_used
#         factory.ore_used = times * factory.ore_used
#         fuel_produced = times * fuel_produced
#         loop_found = True

#     prev_states[key] = fuel_produced

##################################
# Bisection
##################################
low = 1
high = ore_available
n = 0
prev_low = None
prev_high = None

while True:
    n = math.ceil((low + high) / 2)
    factory = NanoFactory(input=input)
    factory.build('FUEL', n)

    if factory.ore_used < ore_available:
        low = n
    elif factory.ore_used > ore_available:
        high = n

    if prev_low == low and prev_high == high:
        n -= 1
        break

    prev_low = low
    prev_high = high
    print('[{} - {}] Ore Used {}, fuel {}'.format(low, high, factory.ore_used, n))


print("Part Two : " + str(n))
