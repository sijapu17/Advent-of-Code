#Advent of Code 2024 Day 23

from collections import defaultdict
from itertools import combinations

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-23.txt')
contents = f.read()
input = contents.splitlines()

#input=['a-b','a-c','b-c']
neighbours=defaultdict(set)

for line in input:
    a,b=line.split('-')
    neighbours[a].add(b)
    neighbours[b].add(a)

t_groups=set()

for name, nbs in neighbours.items():
    if name[0]=='t':
        for n_a,n_b in combinations(nbs,2): #For each pair within nbs, test if they are neighbours
            if n_b in neighbours[n_a]:
                t_groups.add(tuple(sorted((name,n_a,n_b))))

print(len(t_groups)) #Part 1

#Find biggest fully-connected cluster using Bron-Kerbosch algorithm
best_cluster=set()
def BronKerbosch(R,P,X):
    global best_cluster
    if len(P)==0 and len(X)==0:
        if len(R)>len(best_cluster):
            best_cluster=R
    for v in P.copy():
        BronKerbosch(R|{v},P&neighbours[v],X&neighbours[v])
        P-={v}
        X|={v}

BronKerbosch(set(),set(neighbours.keys()),set())
print(','.join(sorted(list(best_cluster)))) #Part 2