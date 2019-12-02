# Advent of code Year 2019 Day 2 solution
# Author = seven
# Date = December 2019

with open((__file__.rstrip("code.py")+"input.txt"), 'r') as input_file:
    input = input_file.read()


class Intmemory(object):

    def __init__(self, input):
        self.memory = [int(s) for s in input.split(',')]
        self.ip = 0
        self.isHalt = False
        self.OPMAP = {
            '1': self.add,
            '2': self.mul,
            '99': self.halt,
        }

    def add(self, addr_a, addr_b, addr_out):
        self.memory[addr_out] = self.memory[addr_a] + self.memory[addr_b]

    def mul(self, addr_a, addr_b, addr_out):
        self.memory[addr_out] = self.memory[addr_a] * self.memory[addr_b]

    def halt(self, *args):
        self.isHalt = True

    def proc_instruction(self):
        opcode = str(self.memory[self.ip])
        addr_a = self.memory[self.ip+1]
        addr_b = self.memory[self.ip+2]
        addr_out = self.memory[self.ip+3]

        if opcode not in self.OPMAP:
            raise RuntimeError('Invalid OP')

        print(','.join([str(i) for i in self.memory[self.ip:self.ip+4]]))

        self.OPMAP[opcode](addr_a, addr_b, addr_out)
        # increase ip by number of params used, for now halt should be 1, but halts
        self.ip += 4

    def run(self):
        while not self.isHalt:
            if len(self.memory) <= self.ip + 3:
                raise RuntimeError('Unexpected end of intmemory')
            self.proc_instruction()


proc1 = Intmemory(input)
proc1.memory[1] = 12
proc1.memory[2] = 2
proc1.run()

print("Part One : " + str(proc1.memory[0]))

target = 19690720

noun = 0
verb = 0

while True:
    comp = Intmemory(input)
    comp.memory[1] = noun
    comp.memory[2] = verb
    comp.run()

    if comp.memory[0] == target:
        break

    verb += 1
    if verb > 99:
        noun += 1
        verb = 0

    if noun > 99:
        raise RuntimeError('Exhausted search space')

result = 100 * noun + verb
print("Part Two : "+ str(result))
