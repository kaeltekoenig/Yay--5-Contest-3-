with open('input.txt', 'r') as f:
    first = list(f.readline().strip())
    second = list(f.readline().strip())

f = {}
s = {}

for el in first:
    if el not in f:
        f[el] = 1
    else:
        f[el] += 1

for el in second:
    if el not in s:
        s[el] = 1
    else:
        s[el] += 1


if f == s:
    print('YES')
else:
    print('NO')

