import os
from pathlib import Path

os.environ['LOG_LEVEL'] = 'ERROR'
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
    list_input.append('')
    string_input = input_loader.load_file_as_string(day, sample)
    most = 0
    curr = 0

    top = []
    for line in list_input:
        if line.strip():
            curr += int(line.strip())
            continue

        if len(top) < 3:
            print(top)
            top.append(curr)
            top.sort()
        else:
            print(top)
            for i in reversed(range(len(top))):
                if curr > top[i]:
                    top.pop(0)
                    # top[i] = curr
                    top = top[:i] + [curr] + top[i:]
                    break
        curr = 0


    print('top', top)
    print('top sum', sum(top))
    answer = sum(top)
    print(f"The answer is {answer}\n")

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
