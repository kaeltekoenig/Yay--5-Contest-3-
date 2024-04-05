occurancies = {}

with open('input.txt', 'r') as f:
    for _ in range(3):
        n = int(f.readline())
        nums = set(map(int, f.readline().split()))
        for num in nums:
            if num not in occurancies:
                occurancies[num] = 1
            else:
                occurancies[num] += 1

twos = set()

for k, v in occurancies.items():
    if v > 1:
        twos.add(k)

print(*sorted(twos))
