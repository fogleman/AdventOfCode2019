import fileinput
import heapq
import intcode

def traverse(program):
    buf = []
    gen = intcode.run(program, buf)
    send = lambda d: buf.append(d + 1) or next(gen)
    test = lambda d: send(d) and send([1, 0, 3, 2][d])
    seq, dx, dy = [0, 3, 1, 2], [0, 0, -1, 1], [-1, 1, 0, 0]
    i, p, cells, oxygen = 0, (0, 0), set(), None
    while True:
        l, r = (i - 1) % 4, (i + 1) % 4
        if test(seq[l]):
            i = l # turn left if possible
        elif not test(seq[i]):
            i = r # else turn right if can't go straight
        d = seq[i]
        s = send(d)
        if s == 0:
            continue
        p = (p[0] + dx[d], p[1] + dy[d])
        cells.add(p)
        if s == 2:
            oxygen = p
        if p == (0, 0):
            return cells, oxygen

def shortest_path(cells, source, target):
    seen, queue = set(), [(0, source)]
    while queue:
        d, p = heapq.heappop(queue)
        if p == target:
            return d
        seen.add(p)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            q = (p[0] + dx, p[1] + dy)
            if q in cells and q not in seen:
                heapq.heappush(queue, (d + 1, q))

cells, oxygen = traverse(list(fileinput.input())[0])
print(shortest_path(cells, (0, 0), oxygen))
print(max(shortest_path(cells, cell, oxygen) for cell in cells))
