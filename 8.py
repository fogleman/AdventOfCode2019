import fileinput

w, h = 25, 6
n = w * h

data = list(map(int, list(fileinput.input())[0].strip()))
layers = [data[i:i+n] for i in range(0, len(data), n)]

# part 1
layer = min(layers, key=lambda x: x.count(0))
print(layer.count(1) * layer.count(2))

# part 2
im = [' '] * n
for layer in reversed(layers):
    for i, v in enumerate(layer):
        if v == 0:
            im[i] = ' '
        if v == 1:
            im[i] = 'X'

for i in range(0, len(im), w):
    print(''.join(im[i:i+w]))
