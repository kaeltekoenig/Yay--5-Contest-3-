playlist = {}
favourites = []

with open('input.txt', 'r') as f:
    n = int(f.readline())
    for _ in range(n):
        amount = int(f.readline())
        songs = f.readline().split()
        for song in songs:
            if playlist.get(song):
                playlist[song] += 1
            else:
                playlist[song] = 1

for name, amnt in playlist.items():
    if amnt == n:
        favourites.append(name)            

print(len(favourites))
print(*sorted(favourites))