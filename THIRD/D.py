def find_krepeat(lst):
    occurancies = {}
    for ind, num in enumerate(nums):
        if num not in occurancies:
            occurancies[num] = [ind]
        else:
            if len(occurancies[num]) and ind - abs(occurancies[num][-1]) <= k:
                print('YES')
                return True
            occurancies[num].append(ind)

    print('NO')
    return False


with open('input.txt', 'r') as f:
    n, k = map(int, f.readline().split())
    nums = list(map(int, f.readline().split()))


find_krepeat(nums)