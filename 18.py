from collections import defaultdict
import fileinput
import heapq
import string

def shortest_path(grid, source, target):
    visited = set()
    queue = [(0, source)]
    while queue:
        distance, position = heapq.heappop(queue)
        if position == target:
            return distance
        if position in visited:
            continue
        visited.add(position)
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            q = (position[0] + dx, position[1] + dy)
            if q in visited or q != target and grid[q] != '.':
                continue
            heapq.heappush(queue, (distance + 1, q))

def make_graph(grid):
    graph = defaultdict(list)
    waypoints = [k for k, v in grid.items() if v not in '#.']
    for a in waypoints:
        for b in waypoints:
            if a <= b:
                continue
            d = shortest_path(grid, a, b)
            if d is not None:
                graph[a].append((b, d))
                graph[b].append((a, d))
    return graph

def search(grid):
    graph = make_graph(grid)
    num_keys = sum('a' <= c <= 'z' for c in grid.values())
    positions = tuple(p for p in grid if grid[p] == '@')
    visited = set()
    queue = [(0, positions, frozenset())]
    while queue:
        distance, positions, keys = heapq.heappop(queue)
        if len(keys) == num_keys:
            return distance
        key = (positions, keys)
        if key in visited:
            continue
        visited.add(key)
        for i, position in enumerate(positions):
            for neighbor, cost in graph[position]:
                c = grid[neighbor]
                if 'A' <= c <= 'Z' and c.lower() not in keys:
                    continue
                new_positions = positions[:i] + (neighbor,) + positions[i+1:]
                new_keys = keys | frozenset(c) if 'a' <= c <= 'z' else keys
                if (new_positions, new_keys) in visited:
                    continue
                heapq.heappush(queue, (distance + cost, new_positions, new_keys))

lines = list(fileinput.input())
grid = {(x, y): lines[y][x] for y in range(len(lines))
    for x in range(len(lines[0])) if lines[y][x] not in '\n'}

print(search(grid)) # part 1

x, y = [p for p in grid if grid[p] == '@'][0]
for dy in range(-1, 2):
    for dx in range(-1, 2):
        grid[(x + dx, y + dy)] = '@' if dx and dy else '#'

print(search(grid)) # part 2
