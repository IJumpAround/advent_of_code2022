import math
import os
import time
from functools import reduce
from pathlib import Path
from typing import List, Callable

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger


# - Starting items lists your worry level for each item the monkey is
#   - currently holding in the order they will be inspected.
# - Operation shows how your worry level changes as that monkey inspects
#   - an item. (An operation like new = old * 5 means that your worry level
#   - after the monkey inspected the item is five times whatever your worry level was before inspection.)
# - Test shows how the monkey uses your worry level to decide where to throw an item next.
#   - If true shows what happens with an item if the Test was true.
#   - If false shows what happens with an item if the Test was false.


class Monkey:

    def __init__(self, monkey_number: int, starting_items, operation: callable, test, t, f):
        self.monkey_number = monkey_number
        self._items: List[int] = starting_items
        self.operation: Callable[[int], int] = operation
        self.test = test
        self.t = t
        self.f = f
        self.inspect_count = 0

    # which monkey should I throw this item to?

    def do_test(self, item) -> int:
        if item % self.test == 0:
            return self.t
        else:
            return self.f

    def inspect(self, item, lcm):
        new_worry = self.operation(item) % lcm
        self._items[0] = new_worry
        self.inspect_count += 1
        return new_worry

    def relief(self, item: int, relief_multiplier=1):
        o_item = item
        if relief_multiplier > 1:
            item = math.floor(item / relief_multiplier)
        self._items[self._items.index(o_item)] = item

    def toss(self, item: int, other_monkey: 'Monkey'):
        other_monkey._items.append(item)
        self._items.pop(self._items.index(item))

    def __len__(self):
        return len(self._items)

    @property
    def item(self):
        return self._items[0]

    def __str__(self):
        return f"Monkey {self.monkey_number} holds: {self._items}"

    def __repr__(self):
        return str(self)


def monkey_factory(monkey_str):
    monkey_input = monkey_str.splitlines()

    monkey_number = int(monkey_input[0].split()[-1][:-1])
    starting_items = [int(n.strip()) for n in monkey_input[1].split(':')[1].split(',')]

    operation = monkey_input[2].split(':')[1].strip()
    test = int(monkey_input[3].split()[-1])
    true = int(monkey_input[4].split()[-1])
    false = int(monkey_input[5].split()[-1])

    operation = f"""def operation_fn(old):
           {operation}
           return new
           """
    exec(operation)
    operation = locals()['operation_fn']

    return Monkey(monkey_number, starting_items, operation, test, true, false)


def find_monkey(monkey_number: int, monkeys: List[Monkey]) -> Monkey:
    monkey = next((m for m in monkeys if m.monkey_number == monkey_number))

    return monkey


def monkey_business(monkeys: List[Monkey]):
    business = 1
    top2 = []
    for m in monkeys:
        if len(top2) < 2:
            top2.append(m.inspect_count)
            top2.sort()
        elif m.inspect_count > min(top2):
            top2[0] = m.inspect_count
            top2.sort()
        print(f'Monkey {m.monkey_number} inspected items {m.inspect_count} times')

    return reduce(lambda x, y: x * y, top2)


# return lcmn if worry can be managed
def manage_worry(monkeys: List[Monkey]) -> int:

    items = []
    for m in monkeys:
        items.extend(m._items)

    lcm = math.lcm(*items)
    if lcm == 0:
        return 0

    for m in monkeys:
        for i in range(len(m._items)):
            m._items[i] = m._items[i] // lcm

    return lcm



@time_fn
def solve(day, sample, rounds=20):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    list_input = string_input.split('\n\n')

    monkeys = [monkey_factory(monkey_str) for monkey_str in list_input]
    print(monkeys)
    lcm = math.lcm(*[m.test for m in monkeys])

    print('lcm', lcm)
    assert lcm > 1
    for round_no in range(rounds):
        for i, monkey in enumerate(monkeys):

            while len(monkey) > 0:
                item = monkey.inspect(monkey.item, lcm)
                toss_to = monkey.do_test(item)
                monkey.toss(item, monkeys[toss_to])

        if round_no in (0, 19) or round_no % 1000 == 0:
            print(f'After round {round_no}')
            for m in monkeys:
                print(f'Monkey {m.monkey_number} inspected items {m.inspect_count}')
            print()

    print(f"The answer is {answer}\n")
    mb = monkey_business(monkeys)

    print(f'The amount of Monkey Business after {rounds} rounds is {mb}')
    return answer


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True, rounds=10000)
    solve(_day_num, sample=False, rounds=10000)
