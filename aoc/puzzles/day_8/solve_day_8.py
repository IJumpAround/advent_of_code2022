import os
from dataclasses import dataclass
from pathlib import Path

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


@dataclass
class Coord:
    r: int
    c: int


def is_visible(forest, r,c, way='v'):
    checked_tree = forest[r][c]
    # print(f'starting checking {checked_tree} ({r},{c})')

    asc = True
    visible = True

    if way == 'v':
        pos = Coord(r=0, c=c)
    else:
        pos = Coord(r=r, c=0)

    for i in range(len(forest)):

        # scan has reached same tree we're checking
        if pos.c == c and pos.r == r:
            if visible is True:
                return True
            else:
                visible = True
                asc = False
                if way == 'v':
                    pos.r += 1
                else:
                    pos.c += 1
                continue

        t = forest[pos.r][pos.c]
        # print(f'checking {checked_tree} ({r},{c})')
        # a tree is higher than this one while moving towards the edge, end early because we cannot see the tree
        if t >= checked_tree:
            if asc is False:
                return False
            else:
                visible = False

        if way == 'v':
            pos.r += 1
        else:
            pos.c += 1

    return visible


def trees_visible(forest, r, c, way='v'):
    checked_tree = forest[r][c]
    scenic_score = 1
    pos = Coord(r=r, c=c)
    if way == 'v':
        ranges = [('u', reversed(range(0, r))), ('d', range(r+1, len(forest)))]
    else:
        ranges = [('l', reversed(range(0, c))), ('r', range(c+1, len(forest)))]

    for rng in ranges:
        visible_count = 0
        direction, rng = rng
        for p in rng:

            if way == 'v':
                pos.r = p
            else:
                pos.c = p

            t = forest[pos.r][pos.c]
            # print(f'checking {checked_tree} ({r},{c}) against {t} ({pos}) {direction=}')

            visible_count += 1
            if t >= checked_tree:
                break

        visible_count = visible_count or 1
        # print(f'score {direction=} {visible_count}')
        scenic_score *= visible_count
    return scenic_score


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    visible_trees = dict()
    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    list_input = [[int(i) for i in row] for row in list_input]
    forest = list_input

    visible_count = 0
    best_scenic_score = 0
    for i, row in enumerate(forest):
        for j, tree in enumerate(row):
            scenic_score = 1
            if i == 0 or i == len(forest) - 1 or j == 0 or j== len(forest) - 1:
                continue

            visible = is_visible(forest, i, j)
            scenic_score *= trees_visible(forest, i, j)
            scenic_score *= trees_visible(forest, i, j, 'h')
            best_scenic_score = max(scenic_score, best_scenic_score)
            print(f'{scenic_score=} trees visible from tree {tree} ({i},{j})')
            if not visible:
                visible = is_visible(forest, i, j, 'h')
                # print(f'{tree=} ({i},{j}) visible on horizontal line: {visible}')

            visible_count += int(visible)

    print('interior visible ', visible_count)
    perim = (2 * len(forest) + 2 * len(forest[0])) - 4  # -4 to not count corners twice
    visible_count += perim
    print(f'{visible_count} trees are visible')
    print(f'Best scenic score {best_scenic_score}')
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
