#Advent of Code 2023 Day 23

from collections import deque

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-23.txt')
contents = f.read()
input = contents.splitlines()

map={}
x_max=len(input[0])
y_max=len(input)
s_pos=complex(input[0].index('.'),0)
e_pos=complex(input[-1].index('.'),y_max-1)
alldirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))
slope_dirs={'>':complex(1,0),'<':complex(-1,0),'^':complex(0,-1),'v':complex(0,1)}

#Import map
for j in range(y_max):
    for i in range(x_max):
        map[complex(i,j)]=input[j][i]
map[s_pos-complex(0,1)]='#' #Add wall to avoid leaving the map above start point
map[e_pos+complex(0,1)]='#' #Add wall to avoid leaving the map below end point

class Node(): #Node for BFS Pathfinding
    def __init__(self,pos:complex,steps:int,visited:set) -> None:
        self.pos=pos
        self.steps=steps
        self.visited=visited

    def __str__(self) -> str:
        return(f'N({self.pos},{self.steps})')
    
    def __repr__(self) -> str:
        return(self.__str__())
    
def BFS_part_1(): #BFS along map to find longest path from start to end
    frontier=deque()
    start=Node(s_pos,0,set())
    frontier.append(start)
    max_path=0 #Longest path from start to end found
    while len(frontier)>0:
        #Check oldest node
        current=frontier.popleft()
        if current.pos in current.visited:
            continue
        current.visited.add(current.pos)
        #Create new nodes
        tile=map[current.pos]
        if current.pos==e_pos: #When path reaches end, check length
            #print(f'{current.steps} path found')
            max_path=max(max_path,current.steps)
            continue
        if tile=='.': #From path, can go in any of four directions
            dirs=alldirs
        else: #From slope, can only go in one direction (part 1)
            dirs=[slope_dirs[tile]]
        for d in dirs:
            p=current.pos+d
            if map[p]!='#' and p not in current.visited:
                frontier.append(Node(p,current.steps+1,current.visited.copy()))
    print('All nodes checked')
    return(max_path)

print(BFS_part_1())

#Part 2

#Find all intersections
intersections=set() #Set of intersections
for k,v in map.items():
    if v=='.':
        neighbours=[map[k+d] for d in alldirs]
        if neighbours.count('#')!=2:
            intersections.add(k)

inter_dists={}

#Calculate distance from each intersection to its direct neighbours
def BFS_intersection(s_inter):
    inter_dists[s_inter]={}
    frontier=deque()
    start=Node(s_inter,0,set())
    frontier.append(start)
    while len(frontier)>0:
        #Check oldest node
        current=frontier.popleft()
        if current.pos in current.visited:
            continue
        current.visited.add(current.pos)
        #Create new nodes
        tile=map[current.pos]
        if current.pos in intersections and current.pos!=s_inter: #When path reaches another intersection, add length to inter_dists dictionary
            inter_dists[s_inter][current.pos]=current.steps
            continue
        for d in alldirs:
            p=current.pos+d
            if map[p]!='#' and p not in current.visited:
                frontier.append(Node(p,current.steps+1,current.visited.copy()))

for pos in intersections:
    BFS_intersection(pos)

def BFS_part_2(): #BFS along map to find longest path from start to end, searching from intersection to intersection
    frontier=deque()
    start=Node(s_pos,0,set())
    frontier.append(start)
    max_path=0 #Longest path from start to end found
    while len(frontier)>0:
        #Check oldest node
        current=frontier.popleft()
        if current.pos in current.visited:
            continue
        current.visited.add(current.pos)
        #Create new nodes
        tile=map[current.pos]
        if current.pos==e_pos: #When path reaches end, check length
            #print(f'{current.steps} path found')
            max_path=max(max_path,current.steps)
            continue
        for p, dist in inter_dists[current.pos].items():
            if p not in current.visited:
                frontier.append(Node(p,current.steps+dist,current.visited.copy()))
    print('All nodes checked')
    return(max_path)

print(BFS_part_2())
