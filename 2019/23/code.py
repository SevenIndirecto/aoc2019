#!/usr/bin/env python3

# Advent of code Year 2019 Day 23 solution
# Author = seven
# Date = December 2019

import enum
import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.abspath(__file__))))
from collections import deque
from shared import vm

with open((__file__.rstrip("code.py") + "input.txt"), 'r') as input_file:
    input = input_file.read()


class NIC(vm.VM):
    def __init__(self, program: str, address: int, network: dict, nat: dict):
        self.queue = deque()
        self.address = address
        self.nat = nat
        self.has_booted = False
        self.packet_in = []
        self.packet_out = []
        self.network = network
        super().__init__(program=program, input=vm.IO(), output=vm.IO())

    def send_packet(self, address, packet):
        if address == 255:
            if self.nat['part_one'] is None:
                self.nat['part_one'] = packet[1]
            self.nat['packet'] = packet
        else:
            self.network[address].add_packet(packet)

    def add_packet(self, packet):
        self.queue.append(packet)

    def load_from_input(self, a: vm.Param):
        if not self.has_booted:
            self.input.value = self.address
            self.has_booted = True
        elif len(self.queue) < 1 and len(self.packet_in) < 1:
            self.input.value = -1
        else:
            if len(self.packet_in) == 0:
                self.packet_in = self.queue.popleft()

            self.input.value = self.packet_in.pop(0)

        super().load_from_input(a)

    def store_to_output(self, a: vm.Param):
        super().store_to_output(a)
        self.packet_out.append(self.output.value)

        if len(self.packet_out) == 3:
            address = self.packet_out.pop(0)
            self.send_packet(address, self.packet_out)
            self.packet_out = []

    def is_idle(self):
        idle = len(self.queue) + len(self.packet_in) + len(self.packet_out) == 0
        return idle


network = {}
nat = {'part_one': None, 'y_history': set(), 'packet': None}
for i in range(50):
    network[i] = NIC(program=input, address=i, network=network, nat=nat)

all_devices_idle_count = 0

while True:
    all_devices_are_idle = True

    for device in network.values():
        device.proc_instruction()
        all_devices_are_idle &= device.is_idle()

    if all_devices_are_idle:
        if nat['packet'] is None:
            continue

        if nat['packet'][1] in nat['y_history']:
            print('Part 1: {}'.format(nat['part_one']))
            print('Part 2: {}'.format(nat['packet'][1]))
            break
        network[0].add_packet(nat['packet'])
        nat['y_history'].add(nat['packet'][1])
        nat['packet'] = None

