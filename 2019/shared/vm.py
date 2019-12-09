from itertools import repeat


class IO(object):

    def __init__(self, initial: int = None):
        self.__value = initial

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Param(object):

    def __init__(self, value, mode=0):
        self.value = value
        self.is_positional = mode == 0
        self.is_immediate = mode == 1
        self.is_relative = mode == 2

    def __repr__(self):
        return '[{0}, {1}]'.format(self.value, 'POS' if self.is_positional else 'IMM' if self.is_immediate else 'REL')


class Memory(list):

    def __init__(self, initial: list):
        self.memory = initial
        self.memory_ext = {}

    def set(self, addr: int, value: int):
        if addr < 0:
            raise IndexError('Cannot set, negative address {0}'.format(addr))

        if addr < len(self.memory):
            self.memory[addr] = value
            return

        self.memory_ext[addr] = value

    def get(self, addr: int):
        if addr < 0:
            raise IndexError('Negative address {0}'.format(addr))

        if addr < len(self.memory):
            return self.memory[addr]

        return self.memory_ext.get(addr, 0)


class VM(object):

    def __init__(self, program: str, input: IO, output: IO):
        self.memory = Memory(initial=[int(s) for s in program.split(',')])
        self.ip = 0
        self.is_halt = False
        self.input = input
        self.output = output
        self.OPMAP = {
            '1': (self.add, 3, 'ADD'),
            '2': (self.mul, 3, 'MUL'),
            '3': (self.load_from_input, 1, 'IN'),
            '4': (self.store_to_output, 1, 'OUT'),
            '5': (self.jump_if_true, 2, 'JMT'),
            '6': (self.jump_if_false, 2, 'JMF'),
            '7': (self.less_than, 3, '<'),
            '8': (self.equals, 3, '=='),
            '9': (self.adjust_relative_base_offset, 1, 'RBO'),
            '99': (self.halt, 0, 'HALT'),
        }
        self.history = []
        self.ip_was_modified = False
        self.is_suspended = False
        self.relative_base = 0

    # OPCODES
    def add(self, a: Param, b: Param, out: Param):
        a_val = self.get_param_value(a)
        b_val = self.get_param_value(b)
        self.memory.set(self.get_param_pointer(out), a_val + b_val)

    def mul(self, a: Param, b: Param, out: Param):
        a_val = self.get_param_value(a)
        b_val = self.get_param_value(b)
        self.memory.set(self.get_param_pointer(out), a_val * b_val)

    def load_from_input(self, a: Param):
        self.memory.set(self.get_param_pointer(a), self.input.value)

    def store_to_output(self, a: Param):
        self.output.value = self.get_param_value(a)

    def halt(self):
        self.is_halt = True

    def jump_if_true(self, con: Param, new_ip: Param):
        is_condition_satisifed = not self.get_param_value(con) == 0
        if is_condition_satisifed:
            self.ip = self.get_param_value(new_ip)
            self.ip_was_modified = True

    def jump_if_false(self, con: Param, new_ip: Param):
        is_condition_satisifed = self.get_param_value(con) == 0
        if is_condition_satisifed:
            self.ip = self.get_param_value(new_ip)
            self.ip_was_modified = True

    def less_than(self, a: Param, b: Param, pos: Param):
        is_less = 1 if self.get_param_value(a) < self.get_param_value(b) else 0
        self.memory.set(self.get_param_pointer(pos), is_less)

    def equals(self, a: Param, b: Param, pos: Param):
        is_eq = 1 if self.get_param_value(a) == self.get_param_value(b) else 0
        self.memory.set(self.get_param_pointer(pos), is_eq)

    def adjust_relative_base_offset(self, a: Param):
        self.relative_base += self.get_param_value(a)

    # END OPCODES
    def get_param_value(self, p: Param):
        if p.is_immediate:
            return p.value

        if p.is_positional:
            return self.memory.get(p.value)

        if p.is_relative:
            return self.memory.get(self.relative_base + p.value)

        raise RuntimeError('Invalid param mode {0}'.format(p))

    def get_param_pointer(self, p: Param):
        if p.is_immediate or p.is_positional:
            return p.value
        return self.relative_base + p.value

    def execute(self, op, args):
        log = ((self.ip, self.OPMAP[op][2], ','.join(
            ['{}(val: {})'.format(a, self.get_param_value(a)) for a in args]
        ), 'rb: {}'.format(self.relative_base)))
        # print(log)
        self.history.append(log)
        self.OPMAP[op][0](*args)

    def print_stack_trace(self):
        for op in self.history:
            print(str(op))

    def suspend(self):
        self.is_suspended = True

    def resume(self, id=None):
        self.is_suspended = False
        if self.is_halt:
            raise RuntimeError('Cannot resume from halt state')
        self.run()

    def proc_instruction(self):
        op_call = str(self.memory.get(self.ip))

        if len(op_call) < 3:
            op = op_call
            unparsed_modes = []
        else:
            op = str(int(op_call[-2:]))
            unparsed_modes = [int(m) for m in op_call[-3::-1]]

        if op not in self.OPMAP:
            self.print_stack_trace()
            raise RuntimeError('Invalid OP {0}'.format(op))

        modes = list(repeat(0, self.OPMAP[op][1]))

        if len(unparsed_modes) > 0:
            for i in range(0, len(unparsed_modes)):
                modes[i] = unparsed_modes[i]

        args = []
        offset = 0

        for mode in modes:
            offset += 1
            args.append(Param(value=self.memory.get(self.ip + offset), mode=mode))

        # execute
        self.execute(op, args)

        if not self.ip_was_modified:
            self.ip += 1 + len(modes)

        self.ip_was_modified = False

    def run(self):
        while not self.is_halt and not self.is_suspended:
            self.proc_instruction()
