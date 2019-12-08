#!/usr/bin/env python3

# Advent of code Year 2019 Day 8 solution
# Author = seven
# Date = December 2019

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()

image = []

WIDTH = 25
HEIGHT = 6

pos = 0
row = input[pos:pos+WIDTH]
height = 0
layer = []

while pos < len(input):
    row = [int(pixel) for pixel in input[pos:pos+WIDTH]]
    layer.append(row)

    pos += WIDTH
    height += 1

    if height >= HEIGHT:
        image.append(layer)
        layer = []
        height = 0


def get_digit_count(layer):
    count = [0, 0, 0]
    for row in layer:
        for pixel in row:
            count[pixel] += 1
    return count


lowest_zeroes = None
lowest_checksum = None

for layer in image:
    count = get_digit_count(layer)
    if lowest_zeroes is None or count[0] < lowest_zeroes:
        lowest_zeroes = count[0]
        lowest_checksum = count[1] * count[2]

print("Part One : " + str(lowest_checksum))

decoded = [[2] * WIDTH for _ in range(HEIGHT)]

colors = [0, 1]

for y in range(HEIGHT):
    for x in range(WIDTH):
        for layer in range(len(image)):
            pixel = image[layer][y][x]

            if pixel in colors:
                decoded[y][x] = pixel
                break

print("Part Two : " + str(None))

for y in range(len(decoded)):
    line = ''

    for x in range(len(decoded[y])):
        color = decoded[y][x]
        line += str(color) if color == 1 else ' '

    print(line)

