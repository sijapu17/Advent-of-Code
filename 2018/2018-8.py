#Advent of Code 2018 Day 8

import collections
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-8.txt')
contents = f.read()

#contents='2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
#contents='1 1 0 2 3 7 4'
input = [int(x) for x in contents.split()]

def solveA(input):
    
    print(input)
    total=0
    nChildren=input.popleft()
    nMets=input.popleft()
    for i in range(nChildren):
        tot=solveA(input)
        total+=tot
    
    for j in range(nMets):
        if len(input)>0:
            total += input.pop()
    
    return(total)


#q=collections.deque(input)
#retA=solveA(q)

def parse(data):
    children, metas = data[:2]
    data = data[2:]
    scores = []
    totals = 0

    for i in range(children):
        total, score, data = parse(data)
        totals += total
        scores.append(score)

    totals += sum(data[:metas])

    if children == 0:
        return (totals, sum(data[:metas]), data[metas:])
    else:
        return (
            totals,
            sum(scores[k - 1] for k in data[:metas] if k > 0 and k <= len(scores)),
            data[metas:]
        )

total, value, remaining = parse(input)

print('part 1:', total)
print('part 2:', value)