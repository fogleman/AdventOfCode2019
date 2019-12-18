from collections import defaultdict
from itertools import groupby
import fileinput
import intcode

DIRS = [1j ** i for i in range(4)]
ORIENTATION = dict(zip('>v<^', DIRS))

def parse(program):
    lines = ''.join(map(chr, intcode.run(program))).strip().split('\n')
    cells = [(x, y) for y in range(len(lines))
        for x in range(len(lines[0])) if lines[y][x] not in '.\n']
    sx, sy = [(x, y) for x, y in cells if lines[y][x] != '#'][0]
    return cells, (sx, sy, ORIENTATION[lines[sy][sx]])

def step(x, y, d):
    return (x + int(d.real), y + int(d.imag))

def walk(cells, x, y, d):
    for d, s in zip([d, d * 1j, d * -1j], ['.', 'R.', 'L.']):
        if step(x, y, d) in cells:
            return [s] + walk(cells, *step(x, y, d), d)
    return []

def simplify(seq, i=0, subseqs=[]):
    if i >= len(seq):
        return [','.join(x) for x in subseqs]
    for j in range(len(seq), i, -1):
        if sum(len(x) + 1 for x in seq[i:j]) - 1 <= 20:
            subseqs.append(seq[i:j])
            if len(set(subseqs)) <= 3:
                result = simplify(seq, j, subseqs)
                if result:
                    return result
            subseqs.pop()

def part1(cells):
    return sum(x * y for x, y in cells
        if all(step(x, y, d) in cells for d in DIRS))

def part2(program, seq):
    subseqs = simplify(seq)
    distinct = list(set(subseqs))
    main = ','.join(chr(ord('A') + distinct.index(x)) for x in subseqs)
    lines = [main] + distinct + ['n\n']
    buf = list(map(ord, '\n'.join(lines)))
    program[0] = 2
    return list(intcode.run(program, buf))[-1]

program = list(map(int, list(fileinput.input())[0].split(',')))
cells, pos = parse(program)
seq = tuple(str(len(list(g))) if k == '.' else k
    for k, g in groupby(''.join(walk(cells, *pos))))

print(part1(cells))
print(part2(program, seq))
