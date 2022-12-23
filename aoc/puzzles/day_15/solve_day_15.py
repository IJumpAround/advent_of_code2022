import os
import re
import threading
from collections import defaultdict
from multiprocessing import Process, Queue
from pathlib import Path
from queue import Empty
from typing import Tuple

os.environ['LOG_LEVEL'] = 'ERROR'
from aoc.utils.consts import SAMPLE_FILE, INPUT_FILE
from aoc.utils.measurement import time_fn

from aoc import logger
from aoc.utils import input_loader

L = logger

Point = Tuple[int, int]


def manhattan(p1: Point, p2: Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def do_a_loop(xmin, xmax, xymin, xymax, candidates, q: Queue):
    print(f'{threading.get_ident()} checking x={xmin}-{xmax} y={xymin},{xymax}')
    for i in range(xmin, xmax):
        j = xymin
        while j < xymax:
            nothing = True
            for candidate in candidates:
                sensor, mh_dist = candidate[0], candidate[2]
                dist_to_sensor = manhattan((i, j), sensor)
                if dist_to_sensor <= mh_dist:
                    nothing = False
                    nxt = mh_dist - dist_to_sensor
                    j += nxt
                    break

            if nothing is True:
                print("Found it!", (i, j))
                print("Frequency: ", i*4000000 + j)
                q.put((i, j))
                return

            j += 1
    print(f'{threading.get_ident()} finished checking x={xmin}-{xmax} y={xymin}-{xymax}')

@time_fn
def solve(day, sample, ytarg=10, xymin=0, xymax=20, p1=False):
    print(f"Running with {SAMPLE_FILE if sample else INPUT_FILE}")
    answer = None

    list_input = input_loader.load_file_as_list(day, sample)
    string_input = input_loader.load_file_as_string(day, sample)

    reg = re.compile('x=(?P<x1>-?\d+).*y=(?P<y1>-?\d+).*x=(?P<x2>-?\d+).*y=(?P<y2>-?\d+)')

    xmin, ymin, xmax, ymax = 0, 0, 0, 0

    sensors = []
    beacons = []
    for line in list_input:
        x1, y1, x2, y2 = [int(x) for x in reg.search(line).groups()]

        xmin = min(xmin, x1, x2)
        ymin = min(ymin, y1, y2)
        xmax = max(xmax, x1, x2)
        ymax = max(ymax, y1, y2)

        sensors.append(((x1, y1,), (x2, y2)))
        print(manhattan(*sensors[-1]))
        beacons.append((x2, y2))

    print('x', xmin, '-', xmax, 'y', ymin, '-', ymax)

    candidates = []
    print("Generating candidates")
    for s, b in sensors:
        mh = manhattan(s, b)

        print(f'Sensor {s} has scan range with x edges {s[0]-mh} {s[0]+mh}\ty edges {s[1]+mh} {s[1]-mh}')
        if abs(ytarg - s[1]) <= mh and p1 is True:
            candidates.append((s, b, mh))
        elif p1 is False and s[1] - mh >= xymin or s[0] - mh >= xymin or s[1] + mh <= xymax or s[0] + mh <= xymax:
            print("Including candidate", s)
            candidates.append((s, b, mh))

        print(f'{str(s):>21} | {str(b):>21} | {mh:>10} | {s[0] - mh:>10}')

    print(f'ruled out {len(sensors) - len(candidates)} candidates. {len(candidates)} left')
    left = min([c[0][0] - c[2] for c in candidates])
    right = max([c[0][0] + c[2] for c in candidates])
    up, down = ytarg, ytarg+1
    if xymin or xymax:
        left = xymin
        right = xymax
        up = xymin
        down = xymax

    print("Calculating places the beacon cannot be")
    print(f"checking x={left}-{right} y={up}-{down}")

    q = Queue()
    num_threads = 10
    ranges = xymax // num_threads

    ranges = [(_*ranges, _*ranges + ranges) for _ in range(num_threads)]

    print(ranges)
    threads = [Process(target=do_a_loop, args=(rng[0], rng[1], xymin, xymax, candidates, q)) for rng in ranges]

    for thread in threads:
        thread.start()

    # while threads:
    for thread in threads:

        try:
            ans = q.get_nowait()
            print(ans)
            return
        except Empty:
            pass

        thread.join(timeout=1)


if __name__ == '__main__':
    _day_num = int(Path(__file__).stem.split('_')[-1])
    solve(_day_num, sample=True)
    solve(_day_num, sample=False, ytarg=2000000, xymax=4000000)
