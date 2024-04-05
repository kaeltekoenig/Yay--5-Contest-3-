with open('input.txt', 'r') as f:
    reductions = set(f.readline().split())
    text = f.readline().split()

output = []

for word in text:
    if len(word) > 1:
        for ln in range(1, len(word) + 1):
            if ln == len(word):
                output.append(word)
                break
            elif word[:ln] in reductions:
                output.append(word[:ln])
                break
    else:
        output.append(word)

print(*output)