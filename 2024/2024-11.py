#Advent of Code 2024 Day 11

from collections import defaultdict

#input='125 17'
input='3 386358 86195 85 1267 3752457 0 741'


stones=defaultdict(int) #Count how many stones of each value there are
for n in input.split():
    stones[int(n)]+=1

def update_stones():
    global stones
    new=defaultdict(int)
    for k,v in stones.items():
        if k==0: #Zero stone
            new[1]+=v
        elif len(str(k))%2==0: #Stone with even length
            mid=int(len(str(k))/2)
            new[int(str(k)[:mid])]+=v
            new[int(str(k)[mid:])]+=v
        else:
            new[k*2024]+=v
    stones=new

for n in range(75):
    update_stones()

print(sum(stones.values()))