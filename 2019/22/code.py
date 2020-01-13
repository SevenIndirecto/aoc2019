#!/usr/bin/env python3

# Advent of code Year 2019 Day 22 solution
# Author = seven
# Date = December 2019

from io import StringIO

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


# Naive part one, sweet summer child :D
class SpaceCards(object):

    def __init__(self, size: int):
        self.deck = [i for i in range(size)]
        self.size = size

    def deal_new_stack(self):
        self.deck.reverse()

    def cut(self, n):
        self.deck = self.deck[n:] + self.deck[0:n]

    def deal_inc(self, n):
        ndeck = [None] * self.size
        offset = 0
        pos = 0

        while offset < self.size:
            ndeck[pos] = self.deck[offset]
            pos += n
            pos %= self.size
            offset += 1

        self.deck = ndeck

    def execute(self, cmd: str):
        CUT = 'cut'
        INC = 'deal with increment'

        if cmd.startswith(CUT):
            n = int(cmd[4:])
            self.cut(n)
        elif cmd.startswith(INC):
            n = int(cmd[len(INC)+1:])
            self.deal_inc(n)
        else:
            self.deal_new_stack()


number_to_track = 2019
size = 10007
scards = SpaceCards(size)
for cmd in StringIO(input):
    scards.execute(cmd.rstrip())

print("Part One: " + str(scards.deck.index(number_to_track)))


# Partial Part Two uses CardIndexShuffler.execute(), solved the memory space problem
# by using modular arithmetic functions to process shuffle, but obviously
# does not work for a large number of iterations. Was useful for debugging still.
class CardIndexShuffler(object):

    def __init__(self, size: int, number_to_track: int, cmd_list: str):
        # Composed shuffle will be a single linear transformation composed of
        # the entire shuffle procedure
        self.composed_shuffle = [1, 0]
        self.deck_size = size
        self.idx = number_to_track
        self.init_shuffle_procedure(cmd_list)

    @staticmethod
    def deal_new_stack(idx, deck_size):
        idx = (-1 * idx - 1) % deck_size
        return idx

    @staticmethod
    def cut(n: int, idx: int, deck_size: int):
        idx = (idx - n) % deck_size
        return idx

    @staticmethod
    def deal_inc(n: int, idx: int, deck_size: int):
        idx = n * idx % deck_size
        return idx

    def execute(self, iterations: int = 1):
        for i in range(iterations):
            for cmd_method, cmd_args in self.commands:
                args = cmd_args + [self.idx, self.deck_size]
                self.idx = cmd_method(*args)

    def init_shuffle_procedure(self, cmd_list: str):
        CUT = 'cut'
        INC = 'deal with increment'
        commands = []
        # composed commands / function into a single command / functions
        # f(x) = (ax + b) % self.size
        cc = [1, 0]

        for cmd in StringIO(cmd_list):
            cmd = cmd.rstrip()

            if cmd.startswith(CUT):
                n = int(cmd[4:])
                commands.append((self.cut, [n]))
                a = cc[0]
                b = cc[1] - n
            elif cmd.startswith(INC):
                n = int(cmd[len(INC)+1:])
                commands.append((self.deal_inc, [n]))
                a = n * cc[0]
                b = n * cc[1]
            else:
                commands.append((self.deal_new_stack, []))
                a = -1 * cc[0]
                b = -1 * cc[1] - 1

            cc = [a % size, b % self.deck_size]
        self.commands = commands
        self.composed_shuffle = cc


# Useful for laaaarge exponents:
# Calculate to the power of n, mod m with exponation by squaring
# x^n = (x^(n/2))^2 if % 2 == 0 else x(x^((n-1)/2))^2
def pow_mod(x, n, m):
    if n == 0:
        return 1
    elif n % 2 == 0:
        t = pow_mod(x, n/2, m)
        return t*t % m
    else:
        t = pow_mod(x, (n-1)/2, m)
        return t*t*x % m

"""
BRAIN DUMP:
After composing all the shuffle functions into a single composed_shuffle
we need to compose composed_shuffle with itself "iterations"-times

Let's try expanding a few compositions, f(x), f(f(x)), f(f(f(x)))...

So f(x) = (ax + b) mod p
and f(f(x)) = (a^2*x + a*b + b) mod p
and f(f(f(x))) = (a^3*x + a^2*b + a*b + b) mod p
so... f^n(x) = (a^n*x + b(a^(n-1) + a^(n-2) + ... + a + 1)) mod p

So composing n times:
f^n(x) = (a^n*x + b * (1-a^n)/(1-a)) mod p
(using sum of geometric series to get b*(1-a^n)/(1-a))

To divide in field Z/pZ we need to calculate the inverse of (1-a) mod p, so
let's say c = 1-a
To find the inverse x such that c*x = 1 (mod p) we use
Fermat's little theorem c^(p-1) = 1 (mod p)

So... c*c^(p-2) = c^(p-1) = 1 (mod p) => x = c^(p-2)

=> inverse of (1-a) = (1-a)^(p-2) (all mod p)

So the whole procedure simplifies to:
y = f^n(x) = a^n*x + b * (1-a^n) * (1-a)^(p-2) mod p

But... we need to actually find the x based on y so... re-arrange

x = (y - b * (1-a^n) * (1-a)^(p-2)) * (a^n)^(p-2) mod p

note that inverse of a^n is (a^n)^(p-2)
"""

size = 119315717514047
# number_to_track = 2019
position_to_check = 2020
iterations = 101741582076661
shuffler = CardIndexShuffler(size, number_to_track, cmd_list=input)
# shuffler.execute(iterations)
# print('Execute iterative {}'.format(shuffler.idx))

a, b = tuple(shuffler.composed_shuffle)
p = size
n = iterations

a_to_pow_of_n = pow_mod(a, n, p)

# res = a_to_pow_of_n * number_to_track % p
# res += (b * (1 - a_to_pow_of_n) % p) * pow_mod(1-a, p-2, p) % p
# res %= p!

res = (position_to_check - ((b * (1 - a_to_pow_of_n) % p) * pow_mod(1-a, p-2, p))) % p
res *= pow_mod(a_to_pow_of_n, p-2, p)
res %= p

print('Part Two: {}'.format(res))

