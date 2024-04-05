def find_deltas(crda, crdb):
    xa0, ya0, xa1, ya1 = crda
    xb0, yb0, xb1, yb1 = crdb
    return (xb0 - xa0, yb0 - ya0, xb1 - xa1, yb1 - ya1)


def twist_match(crd):
    x0, y0, x1, y1 = crd
    if y0 > y1:
        return x1, y1, x0, y0
    elif y0 < y1:
        return x0, y0, x1, y1
    elif x0 < x1:
        return x0, y0, x1, y1
    else:
        return x1, y1, x0, y0
    
    
def define_vector(crd):
    x0, y0, x1, y1 = crd
    if y0 == y1:
        return 1
    elif x0 > x1:
        return 2
    elif x0 < x1:
        return 3
    elif x0 == x1:
        return 4


def define_angle(crd):
    x0, y0, x1, y1 = crd
    return x1 - x0, y1 - y0


a = set()
b = set()
deltas = {}

with open('input.txt', 'r') as f:
    n = int(f.readline())
    for _ in range(n):
        x0, y0, x1, y1 = map(int, f.readline().split())
        a.add(twist_match((x0, y0, x1, y1)))
    for _ in range(n):
        x0, y0, x1, y1 = map(int, f.readline().split())
        b.add(twist_match((x0, y0, x1, y1)))

shifts = n

for ma in a:
    for mb in b:
        if define_vector(ma) == define_vector(mb) and define_angle(ma) == define_angle(mb):
            d = find_deltas(ma, mb)
            if d not in deltas:
                deltas[d] = 1
            else:

                deltas[d] += 1


if deltas:
    print(shifts - max(deltas.values()))
else:
    print(shifts)
