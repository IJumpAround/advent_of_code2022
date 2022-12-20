import itertools
import json
import os
from pathlib import Path
from typing import Union, Any

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader


# L = logger


def integer_check(left: int, right: int) -> Union[bool, None]:
    if left == right:
        return None

    return left < right


def list_check(left_list: list, right_list: list) -> Union[bool, None]:
    correct = None
    print('listcheck', left_list, right_list)
    for left, right in itertools.zip_longest(left_list, right_list):
        if right is None and left is not None:  # right ran out of items before left
            return False
        elif left is None and right is not None:
            return True
        correct = dispatch(left, right)
        if correct is not None:
            return correct
    return correct


def one_value_check(left, right) -> Union[bool, None]:
    if type(left) == int:
        left = [left]
    else:
        right = [right]

    return list_check(left, right)


def dispatch(left: Any, right: Any) -> Union[bool, None]:
    print(f'Compare {left} vs {right}')
    tl = type(left)
    tr = type(right)
    if tl == list and tr == list:
        return list_check(left, right)
    elif tl == int and tr == int:
        return integer_check(left, right)
    elif tr == int and tl != int or tr != int and tl == int:
        return one_value_check(left, right)


@time_fn
def solve(day, sample):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)
    divider_packets = [[[2]], [[6]]]
    raw_pairs = string_input.split('\n\n')
    pairs = []

    idx = 1
    answer = 0
    packets = [] + divider_packets
    for p in raw_pairs:
        l, r = p.split('\n')
        left, right = json.loads(l), json.loads(r)

        correct_order = dispatch(left, right)

        packets.extend([left, right] if correct_order is True else [right, left])

        if correct_order is True:
            answer += idx

        idx += 1

    i = 1
    while i < len(packets):
        j = i
        # in_order = dispatch(packets[j-1], packets[j])
        while j > 0 and (in_order := dispatch(packets[j - 1], packets[j])) is False:
            t = packets[j]
            packets[j] = packets[j - 1]
            packets[j - 1] = t
            j = j - 1

        i += 1

    i1, i2 = packets.index(divider_packets[0]) + 1, packets.index(divider_packets[1]) + 1
    # for i in range(len(packets)):
    #     correct_order = dispatch(divider_packets[0], packets[i])
    #     if
    # i = 1 while i < len()
    print('sorted packets')
    for p in packets: print(p)
    print(f"The answer is {answer}\n")
    print(f'divider packets at indexes {i1}, {i2}, {i1*i2}')

    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False)
