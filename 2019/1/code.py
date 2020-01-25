#!/usr/bin/env python3

# Advent of code Year 2019 Day 1 solution
# Author = seven
# Date = December 2019
from io import StringIO

with open((__file__.rstrip("code.py")+"input.txt"), 'r') as input_file:
    input = input_file.read()


def fuel_for_mass(mass):
    return int(mass) // 3 - 2


total_fuel = sum([fuel_for_mass(module) for module in StringIO(input)])
print("Part One : " + str(total_fuel))


def fuel_for_mass_with_fuel(mass):
    total_fuel = 0
    fuel_for_fuel = fuel_for_mass(mass)

    while fuel_for_fuel > 0:
        total_fuel += fuel_for_fuel
        fuel_for_fuel = fuel_for_mass(fuel_for_fuel)

    return total_fuel


total_fuel = sum([fuel_for_mass_with_fuel(mass) for mass in StringIO(input)])
print("Part Two : " + str(total_fuel))

