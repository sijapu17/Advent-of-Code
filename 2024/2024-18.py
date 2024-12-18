#Advent of Code 2024 Day 18

from dataclasses import dataclass
from collections import deque

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-18.txt')
contents = f.read()
input = contents.splitlines()

x_max=70
y_max=70

dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))

def in_range(pos:complex):
    return(0<=pos.real<=x_max and 0<=pos.imag<=y_max)

def corrupt_bytes(n): #Add first n bytes
    bytes=set()
    for i in range(n):
        rl, im=input[i].split(',')
        bytes.add(complex(int(rl),int(im)))
    return(bytes)


@dataclass
class Node(): #Node for BFS Pathfinding
    pos:complex
    steps:int

def BFS(n):
    bytes=corrupt_bytes(n)
    frontier=deque()
    frontier.append(Node(0,0))
    visited=set()
    while len(frontier)>0:
        current=frontier.popleft()
        if current.pos in visited:
            continue
        visited.add(current.pos)
        if current.pos==complex(x_max,y_max):
            return(current.steps)
        #Create new nodes
        for d in dirs:
            new_pos=current.pos+d
            if new_pos not in bytes and in_range(new_pos):
                frontier.append(Node(new_pos,current.steps+1))
    return(None)

print(BFS(1024))

higest_path=0
lowest_nopath=len(input)
while higest_path+1<lowest_nopath:
    mid=int(higest_path+lowest_nopath)//2
    #print(f'L={higest_path} M={mid} U={lowest_nopath}')
    if BFS(mid) is None: #If midpoint has no path, reduce lowest_nopath
        lowest_nopath=mid
    else:
        higest_path=mid #If midpoint has path, increase higest_path
print(input[lowest_nopath-1])