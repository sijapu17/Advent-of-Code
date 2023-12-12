#Advent of Code 2023 Day 10

from collections import deque
from itertools import product

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-10.txt')
contents = f.read()
input = contents.splitlines()

shapes={} #Convert each symbol into a 3x3 shape
shapes['|']=['.#.','.#.','.#.']
shapes['-']=['...','###','...']
shapes['L']=['.#.','.##','...']
shapes['J']=['.#.','##.','...']
shapes['7']=['...','##.','.#.']
shapes['F']=['...','.##','.#.']
shapes['.']=['...','...','...']
shapes['S']=['.#.','###','.#.']

dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))

def on_pipe(i,j,maptype): #Bool for whether a given coordinate is on any pipe
    if 0<=i<=len(maptype[0])-1 and 0<=j<=len(maptype)-1:
        return(maptype[j][i]=='#')
    else:
        return(False)

map=[] #Map of 3x3 shapes    
for j in range(len(input)):
    rows=['','',''] #3 empty rows
    for i in range(len(input[j])) :
        shape=shapes[input[j][i]]
        if input[j][i]=='S':
            s_pos=complex(3*i+1,3*j+1) #Start coordinate
        for n in range(3):
            rows[n]+=(shape[n])
    for n in range(3):
        map.append(rows[n])

def print_map(map):
    ret=''
    for j in range(len(map)):
        for i in range(len(map[0])):
            ret+='#' if on_pipe(i,j,map) else '.'
        ret+='\n'
    print(ret)

class Node(): #Node for BFS part 1
    def __init__(self,pos,prev,steps,path) -> None:
        self.pos=pos
        self.prev=prev
        self.steps=steps
        self.path=path #Unordered points visited

    def __str__(self) -> str:
        return(f'Node(pos={self.pos},prev={self.prev},steps={self.steps})')
    
    def __repr__(self) -> str:
        return(self.__str__())
    
def BFS_loop(): #BFS along map to find midpoint of loop
    frontier=deque()
    start=Node(s_pos,None,0,set([s_pos]))
    frontier.append(start)
    visited=set()
    paths={} #Record of path for each visited position
    global points_on_loop
    while len(frontier)>0:
        #Check oldest node
        current=frontier.popleft()
        if current.pos in visited:
            points_on_loop=current.path|paths[current.pos]|set([current.pos])
            return(current)
        visited.add(current.pos)
        paths[current.pos]=current.path
        #Create new nodes
        for d in dirs:
            p1=current.pos+d
            p2=current.pos+2*d
            p3=current.pos+3*d
            #Check if path exists from current position to 3 spaces away
            if on_pipe(int(p1.real),int(p1.imag),map) and on_pipe(int(p2.real),int(p2.imag),map) and p3 not in visited:
                frontier.append(Node(p3,current.pos,current.steps+1,current.path|set([current.pos])))
    return('All nodes checked, no solution found')

solution=BFS_loop() #BFS along map to find midpoint of loop

def clean_map(map): #Clear map of any pipes that aren't part of main loop
    cleaned=map.copy()
    for j in range(1,len(map),3):
        for i in range(1,len(map[0]),3):
            if complex(i,j) not in points_on_loop:
                #Set all points in 3x3 block around central point to '.'
                for a in (-1,0,1):
                    cleaned[j+a]=cleaned[j+a][:i-1]+'...'+cleaned[j+a][i+2:]
    return(cleaned)

cleaned=clean_map(map)

class Node2(): #Node for BFS part 2
    def __init__(self,pos) -> None:
        self.pos=pos

    def __str__(self) -> str:
        return(f'Node(pos={self.pos})')
    
    def __repr__(self) -> str:
        return(self.__str__())
    
def BFS_fill(): #BFS along map to find fill area of loop
    #Choose starting position
    starts=(s_pos+complex(1,1),s_pos+complex(1,-1),s_pos+complex(-1,1),s_pos+complex(-1,-1))
    #Try BFS from each start position, moving on if BFS leaves bounds of map
    global visited 
    global points
    for s in starts:
        frontier=deque()
        start=Node2(s)
        frontier.append(start)
        visited=set()
        in_bounds=True
        n=0
        while len(frontier)>0 and in_bounds==True and n<100000:
            #Check oldest node
            current=frontier.popleft()
            n+=1
            if n%1000==1:
                print(f'Node {n}: {current}')
            if not(0<=int(current.pos.real)<=len(map[0])-1 and 0<=int(current.pos.imag)<=len(map)-1):
                in_bounds=False
                break
            visited.add(current.pos)
            #Create new nodes
            for d in dirs:
                p1=current.pos+d
                #Check if adjacent space is not in loop
                if not on_pipe(int(p1.real),int(p1.imag),cleaned) and p1 not in visited:
                    frontier.append(Node2(p1))
                    visited.add(p1)
        #print(visited)
        if in_bounds:
            #Calculate area
            points=[x for x in visited if x.real%3==1 and x.imag%3==1]
            print(f'{s}: {len(points)}')
            #return(len(points))
        else:
            print(f'{s} outside of loop')

print(BFS_fill())
#47 incorrect

def print_fill():
    ret=''
    for j in range(len(map)):
        for i in range(len(map[0])):
            if complex(i,j) in points:
                ret+='*'            
            elif complex(i,j) in visited:
                ret+='~'
            else:
                ret+='#' if on_pipe(i,j,cleaned) else '.'
        ret+='\n'
    print(ret)

#print_fill()