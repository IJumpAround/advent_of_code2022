import os
from pathlib import Path

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    shape_score = 0
    shape_scores = []
    vs_scores = []
    total = 0
    value = {
        0: 1,  # 'A'
        1: 2,  # 'B'
        2: 3   # 'C'
    }

    for op, my in [(line.split()) for line in list_input]:
        print(op, my)
        # if my == 'Y': # paper
        #     shape_score = 2
        # elif my == 'X': # rock
        #     shape_score = 1
        # else: # scissors 'Y'
        #     shape_score = 3
        if my == 'Y':    # draw
            mod_inc = 0
        elif my == 'X':  # lose
            mod_inc = 2
        else:            # 'Z' win
            mod_inc = 1

        t = ord(op) - 65
        m = (t + mod_inc) % 3

        shape_score = value[m]
        if m == t:
            vs_score = 3
        elif m == (t + 1) % 3:
            vs_score = 6
        else:
            vs_score = 0


        total += vs_score + shape_score
        print(f'Round: {op} {my}. {shape_score=} {vs_score=}, total: {shape_score + vs_score}')
    print('total score', total)

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
