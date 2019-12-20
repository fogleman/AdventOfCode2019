from collections import defaultdict
import fileinput
import heapq

def find_portals(grid):
    portals = defaultdict(list)
    delta = lambda x: 1 if x == '' else -1
    for x, y in grid:
        for u, v in [(1, 0), (0, 1)]:
            s = [grid.get((x + d*u, y + d*v), '') for d in [0, 1, 2, 3, -1]]
            a = ['A' <= c <= 'Z' for c in s]
            if s[0] == '.' and a[1] and a[2]:
                portals[s[1]+s[2]].append((x, y, delta(s[3])))
            if a[0] and a[1] and s[2] == '.':
                x, y = x + 2*u, y + 2*v
                portals[s[0]+s[1]].append((x, y, delta(s[-1])))
    aa = portals.pop('AA')[0]
    zz = portals.pop('ZZ')[0]
    result = {}
    for a, b in portals.values():
        result[a[:2]] = b
        result[b[:2]] = a
    return result, aa, zz

def shortest_path(grid, portals, source, target, use_depth):
    visited = set()
    queue = [(0, source)]
    while queue:
        distance, position = heapq.heappop(queue)
        if position == target:
            return distance
        if position in visited:
            continue
        visited.add(position)
        x, y, d = position
        neighbors = [(x + dx, y + dy, d)
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]]
        if (x, y) in portals:
            nx, ny, delta = portals[(x, y)]
            neighbors.append((nx, ny, d + delta * use_depth))
        for q in neighbors:
            if q in visited or grid[q[:2]] != '.' or q[-1] <= 0:
                continue
            heapq.heappush(queue, (distance + 1, q))

lines = list(fileinput.input())
grid = {(x, y): lines[y][x] for y in range(len(lines))
    for x in range(len(lines[0]) - 1)}
portals, aa, zz = find_portals(grid)

print(shortest_path(grid, portals, aa, zz, 0))
print(shortest_path(grid, portals, aa, zz, 1))
