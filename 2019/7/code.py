#!/usr/bin/env python3

# Advent of code Year 2019 Day 7 solution
# Author = seven
# Date = December 2019

import itertools
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from shared import vm

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class AmpIO(vm.IO):

    def __init__(self, initial: int, phase: int):
        self.was_phase_read = False
        self.phase = phase
        super().__init__(initial=initial)

    @vm.IO.value.getter
    def value(self):
        if self.was_phase_read:
            return super().value

        self.was_phase_read = True
        return self.phase


class SuspendableOutputVM(vm.VM):
    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)
        self.suspend()


max_out = None
max_phases = None

for permutation in itertools.permutations([0, 1, 2, 3, 4]):
    last_out = 0

    for phase in permutation:
        amp = AmpIO(initial=last_out, phase=phase)
        proc = SuspendableOutputVM(program=input, input=amp, output=amp)
        proc.run()
        last_out = proc.output.value

    if max_out is None or last_out > max_out:
        max_out = last_out
        max_phases = '{0}'.format(permutation)

print('Max amplify at phase setting: {0}'.format(max_phases))
print('Part One: {0}'.format(max_out))


max_out = None
max_phases = None

for permutation in itertools.permutations([5, 6, 7, 8, 9]):
    last_out = 0

    amps = []
    vms = []

    for phase in permutation:
        amps.append(AmpIO(initial=None, phase=phase))

    amps[0].value = 0

    # Create machines and hookup amps
    for i in range(0, 5):
        in_amp = amps[i]
        out_amp = amps[0] if i == 4 else amps[i+1]
        vms.append(SuspendableOutputVM(program=input, input=in_amp, output=out_amp))

    last_ran_index = 0
    while True:
        vms[last_ran_index].resume(last_ran_index)
        if vms[last_ran_index].is_halt:
            break
        last_ran_index = (last_ran_index + 1) % 5

    last_out = vms[4].output.value

    if max_out is None or last_out > max_out:
        max_out = last_out
        max_phases = '{0}'.format(permutation)

print('Max amplify at phase setting: {0}'.format(max_phases))
print('Part Two: {0}'.format(max_out))

