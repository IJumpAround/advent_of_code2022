import os
from functools import reduce
from pathlib import Path

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


def rucksack_common_element(sack):
    c1 = sack[:len(sack) // 2]
    c2 = sack[len(sack) // 2:]

    s1 = set(c1)
    s2 = set(c2)
    return s1 & s2

def item_to_priority(item):
    x_int = ord(item)
    if x_int >= 97:
        x_int = x_int - 96
    elif x_int >= 65:
        x_int = x_int - (65 - 27)

    return x_int

@time_fn
def solve(day, sample, badges=True):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    s = 0
    buffer = []
    for sack in list_input:
        buffer.append(sack)
        if len(buffer) != 3:
            continue

        badge = [set(line) for line in buffer]
        badge = reduce(lambda x, y: x & y, badge)
        badge = badge.pop()

        if badges:
            priority = item_to_priority(badge)
            s += priority
            print('badge=', badge, ':', priority)
        else:

            for line in buffer:
                c1 = line[:len(line) // 2]
                c2 = line[len(line) // 2:]

                s1 = set(c1)
                s2 = set(c2)

                x = (s1 & s2)
                x = (x - {badge})
                x = x.pop()

                x_int = item_to_priority(x)
                s += x_int
                print(x, x_int)

            answer = s
            print(f"The answer is {answer}\n")

        buffer = []

    answer = s
    print('badges score=', s)
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
