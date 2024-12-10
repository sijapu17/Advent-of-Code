#Advent of Code 2024 Day 10

from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-10.txt')
contents = f.read()
input = contents.splitlines()

map=defaultdict(str)
x_max=len(input[0])
y_max=len(input)
dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))
trailheads=[] #List of coords of all zeroes

#Import map, noting position of all zeroes
for j in range(y_max):
    for i in range(x_max):
        if input[j][i]=='.':
            map[complex(i,j)]=-1
        else:
            map[complex(i,j)]=int(input[j][i])
        if input[j][i]=='0':
            trailheads.append(complex(i,j))

class Node(): #Node for BFS Pathfinding
    def __init__(self,pos:complex,trailhead:complex,val:int,path:tuple) -> None:
        self.pos=pos
        self.trailhead=trailhead #Starting point of trail
        self.val=val
        self.path=path

    def __str__(self) -> str:
        return(f'N({self.pos},{self.val})')
    
    def __repr__(self) -> str:
        return(self.__str__())
    
def DFS(trailheads): #DFS along map to find all peaks and trails
    frontier=[]
    peaks={z:set() for z in trailheads} #Count distinct peaks per trail
    trails={z:set() for z in trailheads} #Count distinct trails
    for z in trailheads:
        frontier.append(Node(z,z,0,tuple([z])))
    trailheads=set()
    while len(frontier)>0:
        #Check node
        current=frontier.pop()
        if current.val==9:
            peaks[current.trailhead].add(current.pos)
            trails[current.trailhead].add(current.path)
            #print(current.path)
        else:
        #Create new nodes
            for d in dirs:
                p=current.pos+d
                if map[p]==current.val+1:
                    frontier.append(Node(p,current.trailhead,current.val+1,current.path+tuple([p])))
    print('All nodes checked')
    print(sum([len(x) for x in peaks.values()]))
    print(sum([len(x) for x in trails.values()]))    
    return()

DFS(trailheads)
#824 too low