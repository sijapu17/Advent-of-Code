#Advent of Code 2024 Day 8

from collections import defaultdict
from itertools import combinations

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-08.txt')
contents = f.read()
input = contents.splitlines()

nodes=defaultdict(list) #Coords of nodes
antinodes_1=set()
antinodes_2=set()
x_max=len(input[0])
y_max=len(input)

#Import map
for j in range(y_max):
    for i in range(x_max):
        if input[j][i]!='.':
            nodes[input[j][i]].append(complex(i,j))

def in_range(pos:complex):
    return(0<=pos.real<x_max and 0<=pos.imag<y_max)

#Find antinodes
for locs in nodes.values():
    for p in combinations(locs,2): #Loop over each pair of nodes within each node type
        diff=p[0]-p[1]
        n=0
        hits=1
        while hits>0:
            hits=0
            for an in p[0]+n*diff, p[1]-n*diff:
                if in_range(an):
                    hits+=1
                    if n==1:
                        antinodes_1.add(an)
                    antinodes_2.add(an)
            n+=1

print(len(antinodes_1))
print(len(antinodes_2))
