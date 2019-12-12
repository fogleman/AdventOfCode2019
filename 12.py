from collections import namedtuple
from itertools import count
from math import gcd
import fileinput
import re

class Point(namedtuple('Point', ['x', 'y', 'z', 'vx', 'vy', 'vz'])):
    def gravity(self, ps):
        x, y, z, vx, vy, vz = self
        sign = lambda a, b: (a > b) - (a < b)
        for q in ps:
            vx += sign(q.x, x)
            vy += sign(q.y, y)
            vz += sign(q.z, z)
        return Point(x, y, z, vx, vy, vz)

def step(ps):
    return [Point(x + vx, y + vy, z + vz, vx, vy, vz)
        for x, y, z, vx, vy, vz in [p.gravity(ps) for p in ps]]

def part1(ps):
    for i in range(1000):
        ps = step(ps)
    return sum(sum(map(abs, p[:3])) * sum(map(abs, p[3:])) for p in ps)

def part2(ps):
    rates, memos = [0] * 3, [set() for _ in range(3)]
    for i in count():
        keys = [tuple(p[j::3] for p in ps) for j in range(3)]
        rates = [r or k in m and i for r, k, m in zip(rates, keys, memos)]
        if all(rates):
            lcm = lambda a, b: a * b // gcd(a, b)
            return lcm(rates[0], lcm(rates[1], rates[2]))
        for m, k in zip(memos, keys):
            m.add(k)
        ps = step(ps)

ps = [Point(*map(int, re.findall(r'[-\d]+', line)), 0, 0, 0)
    for line in fileinput.input()]
print(part1(ps))
print(part2(ps))
