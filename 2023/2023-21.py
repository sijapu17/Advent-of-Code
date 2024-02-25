#Advent of Code 2023 Day 21

from collections import deque
import numpy as np

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-21.txt')
contents = f.read()
input = contents.splitlines()

rocks=set()
dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))
x_max=len(input[0])
y_max=len(input)

#Import map
for j in range(y_max):
    for i in range(x_max):
        match input[j][i]:
            case 'S':
                start=complex(i,j)
            case '#':
                rocks.add(complex(i,j))

def is_rock(pos,part):
    if part==1:
        return(pos in rocks)
    elif part==2:
        mod_pos=complex(pos.real%x_max,pos.imag%y_max)
        return(mod_pos in rocks)

class Node(): #Node for pathfinding
    def __init__(self,pos:complex,steps:int) -> None:
        self.pos=pos
        self.steps=steps

def count_destinations(n,part): #Count number of tiles that can be reached in exactly 64 steps
    evens=set() #Tiles visited in an even number of moves
    odds=set() #Tiles visited in an even number of moves
    frontier=deque()
    frontier.append(Node(start,0))
    while len(frontier)>0:
        current=frontier.pop()
        parity=current.steps%2
        if (parity==0 and current.pos in evens) or  (parity==1 and current.pos in odds): #Skip node if same pos has already been visited
            continue
        if parity==0:
            evens.add(current.pos)
        else:
            odds.add(current.pos)
        if current.steps<n:
            for d in dirs:
                new_pos=current.pos+d
                if not is_rock(new_pos,part):
                    frontier.appendleft(Node(new_pos,current.steps+1))
    if n%2==0:
        return(len(evens))
    else:
        return(len(odds))

def print_map(evens):
    ret=''
    for j in range(y_max):
        for i in range(x_max):
            pos=complex(i,j)
            if pos in evens:
                ret+='O'
            elif pos in rocks:
                ret+='#'
            elif pos==start:
                ret+='S'
            else:
                ret+='.'
        ret+='\n'
    print(ret)


n_visited=count_destinations(64,1)
print(n_visited)

#Part 2
#Garden dimension is 131x131
#(202300*131)+65=26501365, the target number of steps
#Find number of steps at 3 points, then extrapolate
x_points=np.array([0*131+65,1*131+65,2*131+65])
y_points=np.array([count_destinations(x,2) for x in x_points])
print(x_points,y_points)
poly=np.polyfit(x_points,y_points,2)
print(round(np.polyval(poly,26501365)))