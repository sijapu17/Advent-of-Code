#Advent of Code 2023 Day 25

from collections import defaultdict, Counter, deque
from random import choices

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-25.txt')
contents = f.read()
input = contents.splitlines()

components=defaultdict(list) #Dict of which others each component links to

#Populate dict
for line in input:
    c, links=line.split(': ')
    for link in links.split():
        components[c].append(link)
        components[link].append(c)

class Node(): #BFS node
    def __init__(self,pos,path,wires) -> None:
        self.pos=pos
        self.path=path
        self.wires=wires

def wire_id(a,b): #Generate non-directional ID of wire between two components
    return(tuple(sorted((a,b))))

def find_path(start,end): #Find path from start to end and return list containing wires
    frontier=deque()
    frontier.append(Node(start,set(),[]))
    visited=set()
    while len(frontier)>0:
        current=frontier.popleft()
        if current.pos in visited:
            continue
        visited.add(current.pos)
        if current.pos==end:
            return(current.wires)
        #Loop through connecting components
        for c in components[current.pos]:
            if c not in current.path:
                path=current.path.copy()
                path.add(current.pos)
                wires=current.wires+[wire_id(current.pos,c)]
                frontier.append(Node(c,path,wires))

def most_common_wires(n): #Find 3 most common wires after checking n random paths
    visited=Counter()
    comps_list=list(components.keys())
    for i in range(n):
        comps=choices(comps_list,k=2)
        visited.update(find_path(comps[0],comps[1]))
    return(visited.most_common(3))

to_cut=most_common_wires(300)
print(to_cut)

#Cut 3 most common wires
for wire in to_cut:
    a,b = wire[0]
    components[a].remove(b)
    components[b].remove(a)

def count_size(start): #Count size of network, starting from given component
    visited=set()
    frontier=deque()
    frontier.append(start)
    while len(frontier)>0:
        current=frontier.popleft()
        visited.add(current)
        for c in components[current]:
            if c not in visited:
                frontier.append(c)
    return(len(visited))

n_a=count_size(a)
n_b=count_size(b)
print(f'{n_a} * {n_b} = {n_a*n_b}')

