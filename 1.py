import fileinput

masses = list(map(int, fileinput.input()))

def fuel(x):
    x = x // 3 - 2
    if x <= 0:
        return 0
    return x + fuel(x)

print(sum(x // 3 - 2 for x in masses))
print(sum(map(fuel, masses)))
