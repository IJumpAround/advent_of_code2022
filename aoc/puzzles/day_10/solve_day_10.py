import os
from pathlib import Path
from pprint import pprint
from typing import List

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


# addx - 2cycles
# addx V takes two cycles to complete.
#   **After** two cycles, the X register is increased by the value V. (V can be negative.)
# noop takes one cycle to complete. It has no other effect.

X = 1


def noop():
    pass


def addx(x):
    global X
    # print('addx', x)
    X += x


instructions = {
    'noop': noop,
    'addx': addx,
}

instruction_ticks = {
    'noop': 1,
    'addx': 2
}

instruction_exec_next_tick = {
    'noop': False,
    'addx': True
}

W = 40
H = 6

class Instruction:

    def __init__(self, str_instruct, argument=None):
        self._str_name = str_instruct
        self.callable = instructions[str_instruct]
        self.ticks_required = instruction_ticks[str_instruct]
        self.current_ticks = 0
        self.exec_next_tick = True
        self.argument = argument
        self.execute_count = 0
        self._debug = True
        self.first_execution_cycle = -1

    def tick(self, cycle):
        if self.first_execution_cycle == -1:
            self.first_execution_cycle = cycle
        self.current_ticks += 1

    def should_execute(self, after_tick=False) -> bool:
        if self.exec_next_tick and not after_tick:
            return False
        else:
            return self.current_ticks >= self.ticks_required

    def do_execute(self):
        if self.argument is not None:
            self.callable(self.argument)
        else:
            self.callable()
        self.execute_count += 1

    def done(self):
        assert self.execute_count <= 1
        return self.execute_count == 1

    def __str__(self):
        return repr(self)

    def __repr__(self):
        r = f'{self._str_name}({"" if self.argument is None else self.argument})'
        if self._debug:
            r += f'<ex_at_tick={self.ticks_required}, ticks={self.current_ticks}, first_ex_tick={self.first_execution_cycle}, exc_cnt={self.execute_count}>'
        return r



@time_fn
def solve(day, sample):
    global X
    X = 1
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = list(reversed(input_loader.load_file_as_list(day, sample)))
    string_input = input_loader.load_file_as_string(day, sample)

    cycle = 1

    waiting = []
    executing: List[Instruction] = []
    num_executed = 0
    strength = 0
    finished = []

    row, column = 0, 0
    crt = [[' ' for _ in range(W)] for __ in range(H)]
    while list_input or executing or waiting:
        instruction = list_input.pop().split() if list_input else []
        arg = None

        if len(instruction) > 1:
            arg = int(instruction[1])
        elif len(instruction) == 0 and len(executing) == 0:
            break

        if instruction:
            instruction_name = instruction[0]

            instruction = Instruction(instruction_name, argument=arg)

            if executing or waiting:
                waiting.append(instruction)
            elif not executing:
                executing.append(instruction)
            else:
                raise RuntimeError()
            # executing.append(instruction)

        for fn in executing:
            fn.tick(cycle)


        print(f'{column=} {row=}, {X=}')
        if abs(column - X) <= 1:
            crt[row][column] = '#'


        # print(f'{str(instruction):<44} | {cycle=} {X=:<5} {cycle * X:<5}')
        if (cycle % 40 == 0):
            print(f'{executing[0] if executing else""} {cycle=} {num_executed=} {X=} signal={cycle}x{X} = {cycle * X}')
            # print(executing[0] if executing else'')
            row += 1
            column = -1
            strength += cycle * X
        elif cycle > 240:
            break


        assert len(executing) <= 1


        # End of cycle execution
        for fn in executing:
            if fn.should_execute(after_tick=True):
                # print('executed post tick', fn, f'{X=} {cycle=} {cycle * X}')
                fn.do_execute()
                num_executed += 1
                break

        cycle += 1
        column += 1
        executing = [fn for fn in executing if not fn.done()]
        if not executing and waiting:
            executing.append(waiting.pop(0))

    # print(f'{cycle=} {X=} {cycle * X}')
    print(f"The answer is {strength}\n")
    print(crt)
    for row in crt:
        print(''.join(row))

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
