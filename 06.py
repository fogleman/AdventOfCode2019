import fileinput

parent = dict(reversed(line.strip().split(')'))
    for line in fileinput.input())

todo = set(parent)
path = {'COM': []}
while todo:
    for c in list(todo):
        p = parent[c]
        if p in path:
            path[c] = [p] + path[p]
            todo.remove(c)

print(sum(map(len, path.values())))

s1 = list(path['YOU'])
s2 = list(path['SAN'])
while s1[-1] == s2[-1]:
    s1.pop()
    s2.pop()

print(len(s1) + len(s2))
