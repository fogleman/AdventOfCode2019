import fileinput
import intcode
import time

def render(grid):
    xs, ys = zip(*grid)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = ' #x-o'[grid.get((x, y), 0)]
            print(c, end='')
        print()

def part1(program):
    return list(intcode.run(program))[2::3].count(2)

def part2(program, watch):
    program[0] = 2
    buf, grid, score, px = [], {}, 0, 0
    gen = intcode.run(program, buf)
    while True:
        try:
            x, y, t = next(gen), next(gen), next(gen)
        except Exception:
            return score
        if x < 0:
            score = t
            continue
        grid[(x, y)] = t
        if t == 3:
            px = x
        if t == 4:
            buf.append((x > px) - (x < px))
            if watch:
                print('\n' * 40, score)
                render(grid)
                time.sleep(0.1)

program = list(map(int, list(fileinput.input())[0].split(',')))
print(part1(program))
print(part2(program, watch=True))
