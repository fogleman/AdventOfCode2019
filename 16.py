import fileinput

def step(values):
    result = []
    seq = [0, 1, 0, -1]
    for r in range(1, len(values) + 1):
        result.append(abs(sum(v * seq[((i + 1) // r) % 4]
            for i, v in enumerate(values))) % 10)
    return result

def part1(values):
    for i in range(100):
        values = step(values)
    return ''.join(map(str, values[:8]))

def part2(values):
    offset = int(''.join(map(str, values[:7])))
    values = values * 10000
    for p in range(100):
        for i in range(len(values) - 2, offset - 1, -1):
            values[i] = (values[i] + values[i + 1]) % 10
    return ''.join(map(str, values[offset:offset+8]))    

values = list(map(int, list(fileinput.input())[0].strip()))
print(part1(values))
print(part2(values))
