import os
from collections import deque
from pathlib import Path

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


@time_fn
def solve(day, sample, marker_length=14):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    seen = []
    for i, c in enumerate(string_input):

        if len(seen) == marker_length:
            preamble = True
            for j, c2 in enumerate(seen):
                if c2 in seen[j+1:]:
                    preamble = False
                    break
            if preamble:
                answer = i
                break

            seen.pop(0)
            seen.append(c)
        else:
            seen.append(c)




    print(f"The answer is {answer}\n")

    return answer

if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
