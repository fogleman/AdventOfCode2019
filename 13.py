from collections import defaultdict
import fileinput
import intcode
import time

program = list(fileinput.input())[0]

def render(grid):
    xs, ys = zip(*grid)
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            c = grid.get((x, y), '.')
            print(c, end='')
        print()

# tiles = list(intcode.run(program, []))
# print(tiles[2::3].count(2))

sprites = ' #x-o'
grid = {}
scores = []

class Joystick:
    def __init__(self, buf):
        self.buf = buf
    def pop(self, index):
        if not self.buf:
            render(grid)
            print(scores)
            print()
            x = input('Direction [ASD]: ').upper()
            x = {'A': -1, 'S': 0, 'D': 1}[x]
            self.buf.append(x)
        return self.buf.pop(index)

joystick = Joystick([])
gen = intcode.run(program, joystick)
pbx = pby = 0
bx = by = 0
px = py = 0
# 21
while True:
    x, y, t = next(gen), next(gen), next(gen)
    if x < 0:
        scores.append(t)
        print(scores)
    else:
        grid[(x, y)] = sprites[t]
    if t == 4:
        render(grid)
        # print(scores)
        print()
        # time.sleep(0.01)
        pbx, pby = bx, by
        bx, by = x, y
        dx, dy = bx - pbx, by - pby
        d = 0
        if dy > 0:
            ex = bx + dx * (20 - by)
        else:
            ex = bx
        if ex < px:
            d = -1
        elif ex > px:
            d = 1
        joystick.buf.clear()
        joystick.buf.append(d)
    if t == 3:
        px, py = x, y
