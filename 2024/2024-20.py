#Advent of Code 2024 Day 20

from collections import deque

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-20.txt')
contents = f.read()
input = contents.splitlines()

walls=set()
x_max=len(input[0])
y_max=len(input)
dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))

def in_range(pos:complex):
    return(0<=pos.real<x_max and 0<=pos.imag<y_max)

#Import map
for j in range(y_max):
    for i in range(x_max):
        pos=complex(i,j)
        match input[j][i]:
            case '#':
                walls.add(pos)
            case 'S':
                start=pos
            case 'E':
                end=pos

class Node(): #Node for Djikstra
    def __init__(self,pos,path,steps) -> None:
        self.pos=pos
        self.path=path
        self.steps=steps

    def __lt__(self, other):
        return(self.steps<other.steps)
    
    def __str__(self) -> str:
        return(f'Node(pos={self.pos},steps={self.steps})')
    
    def __repr__(self) -> str:
        return(self.__str__())

#Find initial path from start to end, with no shortcuts
def find_initial_path():
    visited=set()
    frontier=deque() #Search frontier, i.e. nodes that have been created but not yet examined
    node=Node(start,{start:0},0)
    frontier.append(node)
    while len(frontier)>0:
        current=frontier.popleft()
        #print(current)
        if current.pos in visited: #Skip node if already visited
            continue  
        visited.add(current.pos)      
        if current.pos==end:
            return(current)
        #Create new nodes in 4 directions
        for d in dirs:
            new_pos=current.pos+d
            if new_pos in walls:
                continue
            new_steps=current.steps+1
            new_path=current.path.copy() 
            new_path[new_pos]=new_steps           
            frontier.append(Node(new_pos,new_path,new_steps))

path_node=find_initial_path()

#Find potential shortcut start points
def find_shortcuts(path,n):
    short_starts=[]
    for c,s in path.items():
        for i in range(-1*n,n+1):
            for j in range(-1*(n-abs(i)),n-abs(i)+1):
                new_pos=c+complex(i,j)
                if new_pos not in walls and in_range(new_pos) and new_pos!=c:
                    short_starts.append((new_pos,s+abs(i)+abs(j)))
    return(short_starts)

#Part 1
short_starts_1=find_shortcuts(path_node.path,2)
#Part 2
short_starts_2=find_shortcuts(path_node.path,20)


#Check each shortcut to see if it can beat fair score by at least n
def count_quick_shortcuts(path,short_starts,n):
    quick_shortcuts=0
    path_coords=set(path.keys()) #Convert path coords to set for quicker check
    for sc_start, sc_steps in short_starts:
        visited=set()
        frontier=deque() #Search frontier, i.e. nodes that have been created but not yet examined
        node=Node(sc_start,None,sc_steps) #No need to record path
        frontier.append(node)        
        while len(frontier)>0:
            current=frontier.popleft()
            #print(current)
            if current.pos in visited: #Skip node if already visited
                continue  
            visited.add(current.pos)      
            if current.pos in path_coords:
                if current.steps+n<=path[current.pos]:
                    quick_shortcuts+=1
                break
            #Create new nodes in 4 directions
            for d in dirs:
                new_pos=current.pos+d
                if new_pos in walls:
                    continue
                new_steps=current.steps+1           
                frontier.append(Node(new_pos,None,new_steps))
    return(quick_shortcuts)

print(count_quick_shortcuts(path_node.path,short_starts_1,100))
print(count_quick_shortcuts(path_node.path,short_starts_2,100))