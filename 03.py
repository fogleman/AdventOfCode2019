import fileinput

DIRS = {
    'U': (0, -1), 'D': (0, 1),
    'L': (-1, 0), 'R': (1, 0),
}

def parse(line):
    result = {}
    x = y = steps = 0
    for token in line.split(','):
        (dx, dy), n = DIRS[token[0]], int(token[1:])
        for i in range(n):
            x, y, steps = x + dx, y + dy, steps + 1
            result.setdefault((x, y), steps)
    return result

lines = list(fileinput.input())
a = parse(lines[0])
b = parse(lines[1])
x = set(a) & set(b)
print(min(sum(map(abs, p)) for p in x))
print(min(a[k] + b[k] for k in x))
