import fileinput
import intcode

N, S, E, W = (0, -1), (0, 1), (1, 0), (-1, 0)
L = {N: W, E: N, S: E, W: S}
R = {N: E, E: S, S: W, W: N}

def turtle(white):
    x, y, d = 0, 0, N
    grid = {}
    if white:
        grid[(x, y)] = 1
    buf = []
    gen = intcode.run(program, buf)
    while True:
        buf.append(grid.get((x, y), 0))
        try:
            grid[(x, y)] = next(gen)
            d = [L, R][next(gen)][d]
            x, y = x + d[0], y + d[1]
        except StopIteration:
            return grid

def render(grid):
    xs, ys = zip(*grid)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = '*' if grid.get((x, y)) else ' '
            print(c, end='')
        print()

program = list(fileinput.input())[0]
print(len(turtle(False)))
render(turtle(True))
