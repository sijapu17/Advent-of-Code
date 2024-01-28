#Advent of Code 2023 Day 17

import heapq

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-17.txt')
contents = f.read()
input = contents.splitlines()

map={}
x_max=len(input[0])
y_max=len(input)
goal = complex(x_max-1,y_max-1)

#Import map
for j in range(y_max):
    for i in range(x_max):
        map[complex(i,j)]=int(input[j][i])

def in_range(pos:complex):
    return(0<=pos.real<x_max and 0<=pos.imag<y_max)

def man_dist(c1:complex,c2:complex): #Return Manhatten Distance
    return(int(abs(c1.real-c2.real)+abs(c1.imag-c2.imag)))

class Node(): #Node for A* Pathfinding
    def __init__(self,pos:complex,dir:complex,g:int) -> None:
        self.pos=pos
        self.dir=dir
        self.g=g #Heat loss so far
        self.h=man_dist(pos,goal) #Least-case heat loss to end (1 per square)
        self.f=self.g+self.h

    def __lt__(self, other):
        return(self.f<other.f)
    
    def __str__(self):
        return(f'Pos={self.pos} Heat Loss={self.g} h={self.h} f={self.f} Dir={self.dir}')

    def __repr__(self):
        return(self.__str__())
    
def A_star(): #Find best path from start to end using A* algorithm
    visited=set()
    frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
    east_node=Node(0,complex(1,0),0)
    south_node=Node(0,complex(0,1),0)
    heapq.heappush(frontier,east_node)
    heapq.heappush(frontier,south_node)
    i=0
    while len(frontier)>0:
        i+=1
        current=heapq.heappop(frontier)
        #print(current)
        #if i%500==0:
        #    print(f'{i}: {current}')
        state=(current.pos,current.dir)
        if state in visited: #Skip node if same pos/dir combination has already been visited
            continue
        visited.add(state)          
        if current.pos==goal:
            print('SOLUTION FOUND')
            return(current)
        #Create new nodes
        for rot in (complex(0,1),complex(0,-1)): #Two directions of 90deg Rotation
            new_pos=current.pos
            new_dir=current.dir*rot
            new_g=current.g
            for steps in (1,2,3): #Number of steps allowed before a mandatory turn
                new_pos+=new_dir
                if not in_range(new_pos):
                    break
                new_g+=map[new_pos] #Add heat loss from new step
                heapq.heappush(frontier,Node(new_pos,new_dir,new_g))
    print("Empty frontier, no solution found")

def A_star_ultra(): #Find best path from start to end using A* algorithm with ultra crucibles
    visited=set()
    frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
    east_node=Node(0,complex(1,0),0)
    south_node=Node(0,complex(0,1),0)
    heapq.heappush(frontier,east_node)
    heapq.heappush(frontier,south_node)
    i=0
    while len(frontier)>0:
        i+=1
        current=heapq.heappop(frontier)
        #print(current)
        #if i%500==0:
        #    print(f'{i}: {current}')
        state=(current.pos,current.dir)
        if state in visited: #Skip node if same pos/dir combination has already been visited
            continue
        visited.add(state)          
        if current.pos==goal:
            print('SOLUTION FOUND')
            return(current)
        #Create new nodes
        for rot in (complex(0,1),complex(0,-1)): #Two directions of 90deg Rotation
            new_pos=current.pos
            new_dir=current.dir*rot
            new_g=current.g
            for steps in range(1,11): #Number of steps allowed before a mandatory turn
                new_pos+=new_dir
                if not in_range(new_pos):
                    break
                new_g+=map[new_pos] #Add heat loss from new step
                if steps>=4:
                    heapq.heappush(frontier,Node(new_pos,new_dir,new_g))
    print("Empty frontier, no solution found")

solution=A_star()
print(solution)
solution2=A_star_ultra()
print(solution2)