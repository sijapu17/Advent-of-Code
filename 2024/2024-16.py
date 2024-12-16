#Advent of Code 2024 Day 16

import heapq

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-16.txt')
contents = f.read()
input = contents.splitlines()

walls=set()
x_max=len(input[0])
y_max=len(input)
dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))

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
    def __init__(self,pos,dir,path,score) -> None:
        self.pos=pos
        self.dir=dir
        self.path=path
        self.score=score

    def __lt__(self, other):
        return(self.score<other.score)
    
    def __str__(self) -> str:
        return(f'Node(pos={self.pos},dir={self.dir},score={self.score})')
    
    def __repr__(self) -> str:
        return(self.__str__())
    
def print_map():
    ret=''
    for j in range(y_max):
        for i in range(x_max):
            if complex(i,j) in best_paths:
                ret+='O'
            elif complex(i,j) in walls:
                ret+='#'     
            else:
                ret+='.'
        ret+='\n'
    return(ret)

def find_best_score():
    visited={} #Dict of pos/dir states with best score to reach
    frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
    node=Node(start,complex(1,0),set([start]),0)
    heapq.heappush(frontier,node)
    best_paths=set() #Record any joint-best paths
    best_score=None
    while len(frontier)>0:
        current=heapq.heappop(frontier)
        state=(current.pos,current.dir)
        if state not in visited.keys(): #Skip node if same pos/dir combination has already been visited with a lower score
            visited[state]=current.score
        elif visited[state]<current.score:
            continue
        if len(best_paths)>0 and current.score>best_score: #Once a node has a higher score than best completed path, exit
            continue         
        if current.pos==end:
            print('SOLUTION FOUND')
            best_paths|=current.path
            if best_score is None:
                print(f'Best score={current.score}')
                best_score=current.score
            continue
        #Create new nodes by turning (-90, 0 or 90 degrees) and then moving to next intersection
        for rot in (complex(0,1),1,complex(0,-1)): #Two directions of 90deg Rotation
            new_pos=current.pos
            new_dir=current.dir*rot
            new_path=current.path.copy()
            new_score=current.score+1000*(rot!=1) #Add 1000 score if turning
            #Move forward until a wall is hit, or there is an option to turn
            while new_pos+new_dir not in walls:
                new_pos+=new_dir
                new_score+=1
                new_path.add(new_pos)
                if new_pos+new_dir*complex(0,1) not in walls or new_pos+new_dir*complex(0,-1) not in walls:
                    break
            if new_pos!=current.pos: #Add new node to frontier if reindeer has moved
                heapq.heappush(frontier,Node(new_pos,new_dir,new_path,new_score))
    return(best_paths)

best_paths=find_best_score()

print(print_map())
print(len(best_paths))