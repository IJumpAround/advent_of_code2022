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


    answer = 0
    q = list_input
    any_overlap = 0

    for line in q:
        x1, x2 = line.split(',')
        s1, e1 = [int(x) for x in x1.split('-')]
        s2, e2 = [int(x) for x in x2.split('-')]

        if (s1 >= s2 and e1 <= e2) or (s2 >= s1 and e2 <= e1):
            answer += 1
        elif (s2 <= s1 <= e2) or (s1 <= s2 <= e1):
            any_overlap += 1

    print('any', any_overlap)
    print('full', answer)
    answer = any_overlap + answer
    print(f"The answer is {answer}\n")

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
