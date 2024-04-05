def findsqvx(a, b):
    dx = (a[0] - b[0])
    dy = (a[1] - b[1])  
    c1 = (a[0] + dy, a[1] - dx)
    c2 = (a[0] - dy, a[1] + dx)
    d1 = (b[0] + dy, b[1] - dx)
    d2 = (b[0] - dy, b[1] + dx)

    return c1, d1, c2, d2

#######################
vertices = set()

with open('input.txt', 'r') as f:
    n = int(f.readline())
    for _ in range(n):
        x, y = map(int, f.readline().split())
        vertices.add((x, y))
#######################

isAll = False
minneeded = 4
vx1 = tuple()
vx2 = tuple()
vx3 = tuple()

if n > 1:
    for i in vertices:
        if isAll:
            break
        for j in vertices:
            if i == j:
                continue
            p1, p2, r1, r2 = findsqvx(i, j)
            if p1 in vertices and p2 in vertices:
                minneeded = 0
                vx1 = ''
                isAll = True
                break
            elif p1 in vertices:
                minneeded = 1
                vx1 = p2
            elif p2 in vertices:
                minneeded = 1
                vx1 = p1
            elif minneeded > 1:
                minneeded = 2
                vx1 = p1
                vx2 = p2

            if r1 in vertices and r2 in vertices:
                minneeded = 0
                vx1 = ''
                isAll = True
                break
            elif r1 in vertices:
                minneeded = 1
                vx1 = r2
            elif r2 in vertices:
                minneeded = 1
                vx1 = r1
            elif minneeded > 1:
                minneeded = 2
                vx1 = p1
                vx2 = p2
else:
    minneeded = 3 
    vx1 = (x, y + 1)
    vx2 = (x + 1, y + 1)
    vx3 = (x + 1, y)

print(minneeded)
print(*vx1)
if vx2 and minneeded > 1:
    print(*vx2)
if vx3 and minneeded == 3:
    print(*vx3)
