import math
import os
from collections import defaultdict
from pathlib import Path
from typing import Union

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __truediv__(self, other: Union[float, int]):
        return Point(self.x / other, self.y / other)

    def __floordiv__(self, other: Union[float, int]):
        return Point(self.x // other, self.y // other)

    def __sub__(self, other) -> 'Point':
        return Point(self.x - other.x, self.y - other.y)

    def clamp(self, integer=True):
        if self.x == 0:
            x = 0
        elif self.x >= 0.0:
            x = 1
        else:
            x = -1

        if self.y == 0:
            y = 0
        elif self.y >= 0.0:
            y = 1
        else:
            y = -1

        return Point(int(x), y)

    def __abs__(self):
        return math.sqrt(pow(abs(self.x), 2) + pow(abs(self.y), 2))

    def should_move(self, head) -> bool:
        return abs(head.x - self.x) > 1 or abs(head.y - self.y) > 1

    def should_move_diagonal(self, head: 'Point'):
        return abs(head.x - self.x) > 0 and abs(head.y - self.y) > 0

    def unit_vector_to(self, other: 'Point', diag=False) -> 'Point':
        return (other - self) / abs(other - self)

    def __repr__(self):
        return f'({self.x}, {self.y})'


@time_fn
def solve(day, sample, num_knots=10):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    true_head = Point(0, 0)
    knots = [Point(0,0) for _ in range(num_knots - 1)]
    # tail = Point(0, 0)
    visits = defaultdict(int)
    directions = {
        'D': Point(0, -1),
        'U': Point(0, 1),
        'R': Point(1, 0),
        'L': Point(-1, 0)
    }

    visits[(0, 0)] = 1
    for command in list_input:
        print(command)
        d, amount = command.split()
        d = directions[d.upper()]
        amount = int(amount)
        for i in range(amount):
            true_head += d
            print(f'{true_head=}\t{knots[-1]=}')

            for i, tail in enumerate(knots):
                if i > 0:
                    head = knots[i-1]
                else:
                    head = true_head
                if tail.should_move(head):
                    if not tail.should_move_diagonal(head):
                        unit_vector = tail.unit_vector_to(head)
                        # print(unit_vector
                        # )
                        unit_vector = Point(int(unit_vector.x), int(unit_vector.y))
                        tail += unit_vector
                    else:
                        # print('moving diagonal')
                        unit_vector = tail.unit_vector_to(head)
                        # print(unit_vector, unit_vector.clamp())
                        tail += unit_vector.clamp()
                    knots[i] = tail
                    print(f'\tMoved tail {head=}\t{tail=}')

                    if tail == knots[-1]:
                        visits[(tail.y, tail.x)] += 1

    print(visits)
    answer = len(visits)
    print(f"The answer is {answer}\n")

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
