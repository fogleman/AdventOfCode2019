from itertools import groupby
import fileinput
import intcode

DIRS = [1j ** i for i in range(4)]

def parse(program):
    lines = ''.join(map(chr, intcode.run(program))).strip().split('\n')
    cells = [(x, y) for y in range(len(lines))
        for x in range(len(lines[0])) if lines[y][x] not in '.\n']
    sx, sy = [(x, y) for x, y in cells if lines[y][x] != '#'][0]
    return cells, (sx, sy, dict(zip('>v<^', DIRS))[lines[sy][sx]])

def step(x, y, d):
    return (x + int(d.real), y + int(d.imag))

def walk(cells, x, y, d):
    for d, s in zip([d, d * 1j, d * -1j], ['.', 'R.', 'L.']):
        if step(x, y, d) in cells:
            return [s] + (walk(cells, *step(x, y, d), d) or [])

def simplify(seq, i=0, seqs=[]):
    if i >= len(seq):
        return [','.join(x) for x in seqs]
    for j in range(len(seq), i, -1):
        if sum(len(x) + 1 for x in seq[i:j]) - 1 <= 20:
            seqs.append(seq[i:j])
            if len(set(seqs)) <= 3:
                result = simplify(seq, j, seqs)
                if result:
                    return result
            seqs.pop()

def part1(cells):
    return sum(x * y for x, y in cells
        if all(step(x, y, d) in cells for d in DIRS))

def part2(program, seq):
    program[0] = 2
    seqs = simplify(seq)
    distinct = list(set(seqs))
    main = ','.join(chr(ord('A') + distinct.index(x)) for x in seqs)
    lines = [main] + distinct + ['n\n']
    return list(intcode.run(program, '\n'.join(lines)))[-1]

program = list(map(int, list(fileinput.input())[0].split(',')))
cells, pos = parse(program)
seq = tuple(str(len(list(g))) if k == '.' else k
    for k, g in groupby(''.join(walk(cells, *pos))))

print(part1(cells))
print(part2(program, seq))
