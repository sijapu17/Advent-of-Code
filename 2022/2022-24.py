#Advent of Code 2022 Day 24

import heapq
from math import lcm

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-24.txt')
contents = f.read()
input = contents.splitlines()

#Map boundaries
global maxX, maxY, start, goal, dirs, t_syms, cycle_len, map_timeline, leg
maxX=len(input[0])
maxY=len(input)
start=complex(1,0)
goal=complex(maxX-2,maxY-1)
dirs={'N':complex(0,-1),'E':complex(1,0),'S':complex(0,1),'W':complex(-1,0),'X':complex(0,0)}
t_syms={complex(0,-1):'^',complex(1,0):'>',complex(0,1):'v',complex(-1,0):'<'}
cycle_len=lcm(maxX-2,maxY-2) #Lenth of cycle before tornado positions must repeat
leg=1 #Leg of journey

def create_map(input):
    map=set()
    for j in range(maxY):
        for i in range(maxX):
            pos=complex(i,j)
            match input[j][i]:
                case '^':
                    map.add((pos,complex(0,-1)))
                case '>':
                    map.add((pos,complex(1,0)))
                case 'v':
                    map.add((pos,complex(0,1)))
                case '<':
                    map.add((pos,complex(-1,0)))
    return(map)

def step_map(map): #Move each tornado 1 step, creating a new map
    new_map=set()
    for t in map:
        newpos=t[0]+t[1]
        if newpos.real==0:
            newpos=complex(maxX-2,newpos.imag)
        elif newpos.real==maxX-1:
            newpos=complex(1,newpos.imag)
        elif newpos.imag==0:
            newpos=complex(newpos.real,maxY-2)
        elif newpos.imag==maxY-1:
            newpos=complex(newpos.real,1)
        new_map.add((newpos,t[1]))
    return(new_map)

def create_map_timeline(map): #Calculate which spaces are occupied for each timepoint
    map_timeline=[]
    current_map=map
    for t in range(cycle_len):
        map_timeline.append(set([x[0] for x in current_map]))
        current_map=step_map(current_map)
    return(map_timeline)

def in_bounds(pos): #Check if pos is in valley bounds (including start and end spaces)
    return(1<=pos.real<=maxX-2 and (1<=pos.imag<=maxY-2 or pos in (start,goal)))

def man_dist(c1:complex,c2:complex): #Return Manhatten Distance
    return(int(abs(c1.real-c2.real)+abs(c1.imag-c2.imag)))

def print_map(map,elf_pos=start):
    ret=''
    tornados_pos=[x[0] for x in map]
    for j in range(maxY):
        for i in range(maxX):
            pos=complex(i,j)
            if pos==elf_pos:
                ret+='E'
            elif not in_bounds(pos):
                ret+='#'
            elif pos in tornados_pos:
                t_dirs=[x[1] for x in map if x[0]==pos]
                if len(t_dirs)>1:
                    ret+=str(len(t_dirs))
                else:
                    ret+=t_syms[t_dirs[0]]
            else:
                ret+='.'
        ret+='\n'
    print(ret)

def print_map_time(time,elf_pos=start): #Print map timeline at specified timepoint
    ret=''
    tornados_pos=map_timeline[time]
    for j in range(maxY):
        for i in range(maxX):
            pos=complex(i,j)
            if pos==elf_pos:
                ret+='E'
            elif not in_bounds(pos):
                ret+='#'
            elif pos in tornados_pos:
                ret+='T'
            else:
                ret+='.'
        ret+='\n'
    print(ret)

def A_star(legs=3): #Find shortest path from start to end using A* algorithm
        global leg

        visited=set()
        frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
        start_node=Node(start,0,'')
        heapq.heappush(frontier,start_node)
        i=0
        while len(frontier)>0:
            i+=1
            current=heapq.heappop(frontier)
            #print(current)
            #if i%500==0:
            #    print(f'{i}: {current}')
            state=(current.pos,current.g)
            #Skip node if position has already been visited in same number of steps
            #Note that best path may revisit same pos at different steps
            if state in visited:
                continue
            visited.add(state)          
            if (leg%2==1 and current.pos==goal) or (leg%2==0 and current.pos==start):
                print(f'Leg {leg} completed, {current.g} steps taken in total')
                if leg==legs:
                    return(current)
                else: #Reset search for next leg
                    leg+=1
                    frontier=[]
                    visited=set()
            for sym, d in dirs.items():
                new_pos=current.pos+d
                if new_pos not in map_timeline[(current.g+1)%cycle_len] and in_bounds(new_pos):
                    heapq.heappush(frontier,Node(new_pos,current.g+1,current.path+sym))
        print("Empty frontier, no solution found")

class Node():
    def __init__(self,pos:complex,steps:int,path:str) -> None:
        self.pos=pos
        self.path=path
        self.g=steps #Steps so far
        if leg%2==1:
            self.h=man_dist(pos,goal) #Best-case remaining steps to goal on odd legs
        else:
            self.h=man_dist(pos,start) #Best-case remaining steps to start on odd legs
        self.f=self.g+self.h

    def __lt__(self, other):
        return(self.f<other.f)
    
    def __str__(self):
        return(f'Pos={self.pos} Steps={self.g} h={self.h} f={self.f} {self.path}')

    def __repr__(self):
        return(self.__str__())


map=create_map(input)
map_timeline=create_map_timeline(map)
solution=A_star()
print(solution)
