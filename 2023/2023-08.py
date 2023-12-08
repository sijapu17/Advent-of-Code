#Advent of Code 2023 Day 8

import re
from math import lcm

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-08.txt')
contents = f.read()
input = contents.splitlines()

dirs=input[0]
map={}

for row in input[2:]:
    match=re.findall(r"\w{3}",row)
    map[match[0]]={'L':match[1],'R':match[2]}

#Return nth direction in sequence (looping after reaching end)
def nth_dir(n):
    return(dirs[n%len(dirs)])

#Traverse from start to end
def traverse(start,end):
    pos=start
    steps=0
    while pos!=end:
        pos=map[pos][nth_dir(steps)]
        steps+=1
    return(steps)

print(traverse('AAA','ZZZ'))

#Traverse until reaching any nodes ending in z
def traverse_z(start):
    pos=start
    steps=0
    while pos[-1]!='Z':
        pos=map[pos][nth_dir(steps)]
        steps+=1
    return(steps)

#Find LCM of all paths
def traverse_all():
    start_nodes=[x for x in map.keys() if x[-1]=='A']
    LCM=1 #Lowest Common Multiple
    for s in start_nodes:
        LCM=lcm(LCM,traverse_z(s))
    return(LCM)

print(traverse_all())