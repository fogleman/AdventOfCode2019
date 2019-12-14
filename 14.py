from collections import defaultdict
import fileinput
import math
import re

def run(reactions, fuel):
    counts = defaultdict(int, {'FUEL': fuel})
    while True:
        done = True
        ore = 0
        produced = defaultdict(int)
        required = defaultdict(int)
        for k, v in counts.items():
            produced[k] = reactions[k][0] * v
            for n, m in reactions[k][1]:
                required[m] += v * n
        for m, n in required.items():
            if m == 'ORE':
                ore += n
            elif produced[m] < n:
                counts[m] += int(math.ceil(
                    (n - produced[m]) / reactions[m][0]))
                done = False
        if done:
            return ore

def part1(reactions):
    return run(reactions, 1)

def part2(reactions):
    ore = 1000000000000
    lo, hi = 1, ore
    while lo < hi:
        f = (lo + hi) // 2
        if run(reactions, f) <= ore:
            lo = f + 1
        else:
            hi = f - 1
    return lo

reactions = {}
for line in fileinput.input():
    items = [(int(n), m) for n, m in re.findall(r'(\d+) (\w+)', line)]
    count, material = items[-1]
    reactions[material] = (count, items[:-1])

print(part1(reactions))
print(part2(reactions))
