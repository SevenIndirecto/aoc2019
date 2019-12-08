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
        self.is_immediate = mode == 1
        self.is_positional = not self.is_immediate

    def __repr__(self):
        return '[{0}, {1}]'.format(self.value, 'POS' if self.is_positional else 'IMM')


class VM(object):

    def __init__(self, program: str, input: IO, output: IO):
        self.memory = [int(s) for s in program.split(',')]
        self.ip = 0
        self.is_halt = False
        self.input = input
        self.output = output
        self.OPMAP = {
            '1': (self.add, 3),
            '2': (self.mul, 3),
            '3': (self.load_from_input, 1),
            '4': (self.store_to_output, 1),
            '5': (self.jump_if_true, 2),
            '6': (self.jump_if_false, 2),
            '7': (self.less_than, 3),
            '8': (self.equals, 3),
            '99': (self.halt, 0),
        }
        self.history = []
        self.ip_was_modified = False
        self.is_suspended = False

    # OPCODES
    def add(self, a: Param, b: Param, out: Param):
        a_val = self.get_param_value(a)
        b_val = self.get_param_value(b)
        self.memory[out.value] = a_val + b_val

    def mul(self, a: Param, b: Param, out: Param):
        a_val = self.get_param_value(a)
        b_val = self.get_param_value(b)
        self.memory[out.value] = a_val * b_val

    def load_from_input(self, a: Param):
        self.memory[a.value] = self.input.value

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
        self.memory[pos.value] = is_less

    def equals(self, a: Param, b: Param, pos: Param):
        is_eq = 1 if self.get_param_value(a) == self.get_param_value(b) else 0
        self.memory[pos.value] = is_eq

    # END OPCODES
    def get_param_value(self, p: Param):
        p_val = p.value if p.is_immediate else self.memory[p.value]
        return p_val

    def execute(self, op, args):
        self.history.append((op, ','.join([str(a) for a in args])))
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
        op_call = str(self.memory[self.ip])

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
            args.append(Param(value=self.memory[self.ip + offset], mode=mode))

        # execute
        self.execute(op, args)

        if not self.ip_was_modified:
            self.ip += 1 + len(modes)

        self.ip_was_modified = False

    def run(self):
        while not self.is_halt and not self.is_suspended:
            if len(self.memory) <= self.ip:
                raise RuntimeError('Unexpected end of intmemory')
            self.proc_instruction()
