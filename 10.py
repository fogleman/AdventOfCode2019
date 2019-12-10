from math import atan2, hypot, pi
import fileinput

def angle(a, b):
    return atan2(b[0] - a[0], a[1] - b[1]) % (2 * pi)

def visible(asteroids, a):
    return len(set(angle(a, b) for b in asteroids if a != b))

def part1(asteroids):
    return max(visible(asteroids, a) for a in asteroids)

def part2(asteroids):
    a = max(asteroids, key=lambda a: visible(asteroids, a))
    asteroids.remove(a)
    asteroids.sort(key=lambda b: hypot(b[0] - a[0], b[1] - a[1]))
    ranks = {b : sum(angle(a, b) == angle(a, c) for c in asteroids[:i])
        for i, b in enumerate(asteroids)}
    x, y = sorted(asteroids, key=lambda b: (ranks[b], angle(a, b)))[199]
    return x * 100 + y

lines = list(fileinput.input())
asteroids = [(x, y) for y in range(len(lines))
    for x in range(len(lines[0])) if lines[y][x] == '#']

print(part1(asteroids))
print(part2(asteroids))
