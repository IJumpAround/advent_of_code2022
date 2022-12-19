import copy
import os
import sys
from pathlib import Path
from typing import Tuple, List

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger

Vertex = Tuple[Tuple[int, int], str, int]


def is_adj(v1: Vertex, v2: Vertex):
    r1, c1 = v1[0]
    r2, c2 = v2[0]

    return abs(r1 - r2) <= 1 and c1 == c2 or abs(c1 - c2) <= 1 and r1 == r2


# reverse if traveling from the E point towards a lower point
def height_check(src: Vertex, dest: Vertex, reverse=True):

    s1, d1 = src[1], dest[1]
    s1 = s1 if s1 != 'E' else 'z'
    s1 = s1 if s1 != 'S' else 'a'
    d1 = d1 if d1 != 'E' else 'z'
    d1 = d1 if d1 != 'S' else 'a'

    # print(h1, h2)
    if reverse is False:
        return ord(d1) - ord(s1) <= 1
    else:
        return ord(s1) - ord(d1) <= 1


def stringify_node(n: Vertex):
    return f'[{n[2]}] {n[0]} {n[1]}'


def print_matrix(mtx, headers=True):

    h = [str(_) for _ in range(len(mtx))]
    w = max(map(len, h))

    h_str = "".join([f'{_:<{w}}  ' for _ in h])

    if headers:
        print('   | ' + h_str)
    for i, row in enumerate(mtx):
        line = "".join([f"{_:<{w}}  " for _ in row])
        if headers:
            line = f'{i:<3}| ' + line
        print(line)


@time_fn
def solve(day, sample, find_all=True, reverse=True):
    D = {}
    U = {}
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    n = len(list_input) * len(list_input[0])
    mtx = [[0 for _ in range(n)] for __ in range(n)]
    print(f"The answer is {answer}\n")

    V: List[Vertex] = []
    node_num = 0

    if reverse:
        start_char = 'E'
        end_char = 'a'
    else:
        start_char = 'S'
        end_char = 'E'

    for i, r in enumerate(list_input):
        for j, c in enumerate(r):
            V.append(((i, j), c, node_num))

            if c == start_char:
                D[node_num] = 0
            else:
                D[node_num] = sys.maxsize
            node_num += 1

    for v in V:
        print(stringify_node(v))

    SPT = set()
    for i in range(len(V)):
        for j in range(len(V)):

            v1, v2 = V[i], V[j]
            if mtx[v1[2]][v2[2]] == 1:
                continue
            if is_adj(v1, v2):
                allowed_step = int(height_check(v1, v2, reverse=reverse))
                mtx[i][j] = allowed_step
            else:
                mtx[i][j] = 0

    while True:
        dist = [key for key in D if V[key][2] not in SPT]
        if not dist:
            break

        i = min(dist, key=lambda x: D[x])
        u = V[i]
        print('checking neighbors of ', u)
        if u[2] in SPT:
            continue

        SPT.add(u[2])

        for j in range(len(mtx)):
            if j == i:
                continue
            if mtx[i][j] != 1:
                continue
            v = V[j]
            if v[2] in SPT:
                continue
            D[j] = min(D[j], D[i] + 1)

        if u[1] == end_char and not find_all:
            for j in range(len(mtx)):
                if D[j] == sys.maxsize:
                    break
            break

    finished_board = copy.deepcopy(list_input)

    steps = 0
    m = max([len(str(num)) if num != sys.maxsize else 1 for num in D.values()])
    finished_board = [[_ for _ in row] for row in finished_board]
    for s in D:

        r, c = V[s][0]
        row = finished_board[r]
        row = list(row)
        row[c] = str(D[s])
        finished_board[r] = row

    for i, row in enumerate(finished_board):
        row = [str(_) if _ != str(sys.maxsize) else '∞' for _ in row]
        row = " ".join(row)
        finished_board[i] = "".join([f'{_:<{m+1}}' for _ in row.split()])

    print('\noriginal board\n' + "\n".join(list_input))
    print('\nFinished board')
    print("\n".join(finished_board))
    print('steps', steps)

    shortest = sys.maxsize
    for u in V:
        if u[1] == end_char:

            if D[u[2]] == sys.maxsize:
                print(f'Destination node can\'t be reached')
                continue
            print(f'Destination node {stringify_node(u)} can be reached in steps: {D[u[2]]}')
            shortest = min(shortest, D[u[2]])

    print('The shortest path is', shortest)
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
