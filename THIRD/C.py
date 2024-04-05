with open('input.txt', 'r') as f:
    n = int(f.readline())
    array = list(map(int, f.readline().split()))

nums = {}

for n in array:
    if n not in nums:
        nums[n] = 1
    else:
        nums[n] += 1

maxsum = 0
maxpair = []

for n in array:
    if nums.get(n + 1):
        if nums.get(n) + nums.get(n + 1) > maxsum:
            maxsum = nums.get(n) + (nums.get(n + 1))
            maxpair = [n, n + 1]
    else:
        if nums.get(n) > maxsum:
            maxsum = nums.get(n)
            maxpair = [n]     

del nums[maxpair[0]]
if nums.get(maxpair[-1]):
    del nums[maxpair[-1]]

print(sum(nums.values()))