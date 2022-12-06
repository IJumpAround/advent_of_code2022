import os
from collections import defaultdict
from pathlib import Path
from pprint import pprint

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


def load_input(input_list):
    cols = int(input_list[-1].split()[-1])
    print('cols', cols)
    stacks = defaultdict(list)
    for line in input_list[:-1]:
        ptr = 0
        i = 0
        while ptr < 3 * cols + 1 * cols:
            c = line[ptr + 1: ptr + 3 - 1]
            if c.strip():
                stacks[i + 1].append(c)
            i += 1
            ptr = i * 4

    stacks = {k: list(reversed(v)) for k, v in stacks.items()}
    return stacks


@time_fn
def solve(day, sample, v2=True):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    stack_input = []
    idx = 0
    for l in list_input:
        idx += 1
        if l.strip() == '':
            break
        stack_input.append(l)

    command_input = list_input[idx:]
    stack_input = load_input(stack_input)
    pprint(stack_input)

    for cmd_line in command_input:
        cmds = cmd_line.split()
        amt = int(cmds[1])
        origin = int(cmds[3])
        dest = int(cmds[5])

        if not v2:
            for time in range(amt):
                stack_input[dest].append(stack_input[origin].pop())
        else:
            stack_input[dest].extend(stack_input[origin][-amt:])
            stack_input[origin] = stack_input[origin][:-amt]

    print(f"The answer is {answer}\n")

    print('the top of each stack')
    for k in sorted(stack_input):
        print(k, stack_input[k][-1])
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
