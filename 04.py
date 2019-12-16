import fileinput

from itertools import groupby

def valid(code, pred):
    # 599922 => ('5', '9', '2'), (1, 3, 2)
    keys, counts = zip(*[(k, len(list(v))) for k, v in groupby(str(code))])
    return all(b >= a for a, b in zip(keys, keys[1:])) and any(pred(x) for x in counts)

a, b = map(int, list(fileinput.input())[0].split('-'))
print(sum(valid(code, lambda x: x > 1) for code in range(a, b))) # part 1
print(sum(valid(code, lambda x: x == 2) for code in range(a, b))) # part 2
