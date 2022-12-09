import os
import sys
from pathlib import Path

os.environ['LOG_LEVEL'] = 'INFO'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger
TOTAL_DISK = 70000000
NEED_FREE = 30000000


def cd(path: list, dest):
    p = [p for p in path]
    if dest not in ('..', '/'):
        p.append(dest)
    elif dest == '..':
        p.pop()
    else:
        p = []

    return p


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    process(list_input)


def ls(line):
    files = dict()
    if line[0] != 'dir':
        files[line[1]] = int(line[0])

    return files


def total_dir_size(dir_sizes: dict, path: str, current_size, seen: set) -> int:
    # if path == '/':
    # print(f'Calculating total dir size of {path} with current_size {current_size}')

    for d in sorted(dir_sizes, key=lambda x: len(x), reverse=True):
        if current_size > 100000:
            pass
            # raise ValueError()
        # print(d)
        # print(path, d)
        if d.startswith(path) and d != path and d not in seen:
            # print(f'recursion {path=}, {d=}, {current_size=}')
            seen.add(d)
            current_size += total_dir_size(dir_sizes, d, dir_sizes[d], seen)
            # print('size after recursion', current_size)

    return current_size


def process(list_input):
    dir_sizes = dict()
    path = []

    i = 0
    while i < len(list_input):
        line = list_input[i]
        line = line.split()

        if line[0] == '$':  # command
            if line[1] == 'cd':
                path = cd(path, line[2])
            elif line[1] == 'ls':
                line[0] = ' '

                print('LS -----------')
                here_sizes = dict()
                while line[0] != '$' and i < len(list_input) - 1:
                    i += 1
                    line = list_input[i].split()
                    if line[0] == '$':
                        break

                    here_sizes.update(ls(line))
                    if here_sizes:
                        d, s = list(here_sizes.items())[0]
                        print(f'ls {"".join(path)}/{d}: {s}')
                    full_path = "/" + "/".join(path)
                    dir_sizes[full_path] = sum(here_sizes.values())
                print('-------------LS\n')
                continue

        i += 1

    print(dir_sizes)

    answer = sum(dir_sizes.values())

    answer = 0
    total_root_size = total_dir_size(dir_sizes, '/', dir_sizes['/'], set())
    required_to_free = NEED_FREE - (TOTAL_DISK - total_root_size)
    print(f"Need to free {required_to_free}")
    chosen = sys.maxsize
    for d in dir_sizes:
        try:
            ts = total_dir_size(dir_sizes, d, dir_sizes[d], set())

            if required_to_free <= ts < chosen:
                chosen = ts
            print(f'Total dir size of {d}: {ts}')
            answer += ts
        except ValueError:
            pass

    print(f'Delete directory size: {chosen}')
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
