import os
from copy import copy
from pathlib import Path

from aoc.utils.printing import print_matrix

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


def vertical_rest_possible(position, mtx):
    for r in range(position[1] + 1, len(mtx)):
        if mtx[r][position[0]] != '.':
            return True

    return False


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None
    infinite_floor = True
    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    xmax, ymax = 0, 0
    xm, ym = 999, 999

    lines = []
    for line_segments_str in list_input:
        segments = [list(map(int, r_pt.split(','))) for r_pt in line_segments_str.split('->')]
        lines.append(segments)
        for pt in segments:
            xmax = max(xmax, int(pt[0]))
            ymax = max(ymax, int(pt[1]))
            xm = min(xm, int(pt[0]))
            ym = min(ym, int(pt[1]))

    y_extra = 2 if infinite_floor else 0
    mtx = [['.' for _ in range(xmax + 500)] for __ in range(ymax + 1 + y_extra)]

    for line in lines:
        origin = None
        for segment in line:

            if origin is None:
                origin = segment
                mtx[segment[1]][segment[0]] = '#'
                continue

            if origin[1] == segment[1]:  # line is horizontal
                sign = segment[0] - origin[0]
                sign //= abs(sign)

                if sign > 0:
                    x = range(origin[0], segment[0] + 1)
                else:
                    x = range(segment[0], origin[0])
                y = [origin[1]] * len(x)
            elif origin[0] == segment[0]:  # line is vertical
                sign = segment[1] - origin[1]
                sign //= abs(sign)
                if sign > 0:
                    y = range(origin[1], segment[1] + 1)
                else:
                    y = range(segment[1], origin[1])

                x = [origin[0]] * len(y)
            else:
                raise RuntimeError('shit broke')

            for col, row in zip(x, y):
                mtx[row][col] = '#'

            origin = segment

    print_matrix(mtx, row_range=(0, ymax), col_range=(xm, xmax + 1))

    sand_origin = (500, 0)

    sand = None
    print(f'{"*" * 25} Beginning Simulation! {"*" * 25}')
    sand_units = 0
    debug = False
    floor = 2 + ymax

    if infinite_floor:
        for i in range(len(mtx[0])):
            mtx[-1][i] = '#'
    while True:
        if not sand:
            sand = copy(sand_origin)
            sand_units += 1
        mtx[sand[1]][sand[0]] = '+'
        if not vertical_rest_possible(sand, mtx) and infinite_floor is False:
            print(f'Sand {sand} cannot come to rest')
            sand_units -= 1
            break

        sc, sr = sand
        if sr == floor:
            mtx[sr][sc] = 'o'
            sand = None
            continue

        if mtx[sr + 1][sc] == '.':
            sand = (sc, sr + 1)
        elif mtx[sr + 1][sc - 1] == '.':
            sand = (sc - 1, sr + 1)
        elif mtx[sr + 1][sc + 1] == '.':
            sand = (sc + 1, sr + 1)
        else:
            print(f'sand came to rest at {sand}')
            mtx[sr][sc] = 'o'

            if sand == (500, 0):
                print("The hole is plugged!")
                break
            sand = None
            continue

        if debug:
            print_matrix(mtx, row_range=(0, floor), col_range=(xm - 10, xmax + 10))
        mtx[sr][sc] = '.'

    print(f"Amount of sand that came to rest {sand_units}")

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
