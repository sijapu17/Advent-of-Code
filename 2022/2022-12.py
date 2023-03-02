#Advent of Code 2022 Day 12

import heapq
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-12.txt')
contents = f.read()
inp = contents.splitlines()

class Hill():
    def __init__(self,inp) -> None:
        self.dimX=len(inp[0])
        self.dimY=len(inp)
        self.map={}
        self.dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))
        for j in range(self.dimY):
            for i in range(self.dimX):
                val=inp[j][i]
                if val=='S':
                    self.start=complex(i,j)
                    val='a'
                elif val=='E':
                    self.end=complex(i,j)
                    val='z'
                self.map[complex(i,j)]=ord(val)

    def __str__(self) -> str:
        ret=''
        for j in range(self.dimY):
            for i in range(self.dimX):
                if complex(i,j)==self.start:
                    ret+='S'
                elif complex(i,j)==self.end:
                    ret+='E'
                else:
                    ret+=chr(self.map[complex(i,j)])
            ret+='\n'
        return(ret)

    def in_range(self,coord): #Check if a coordinate is within the bounds of the system
        return(0<=coord.real<self.dimX and 0<=coord.imag<self.dimY)

    def find_shortest_path(self,start=None): #Using A* algorithm, find shortest path
        if start==None:
            start=self.start
        frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
        visited=set() #Visited positions
        start_node=Node(start,0,self.end)
        heapq.heappush(frontier,start_node)
        while len(frontier)>0:
            node=heapq.heappop(frontier) #Examine node in open heap with lowest f
            #print(node)
            if node.pos in visited:
                continue
            if node.pos==self.end: #Check if node is the end node
                #print('Solution node found')
                return(node.f)
            else:
                visited.add(node.pos)
                for d in self.dirs: #Create new node in each direction
                    new_pos=node.pos+d
                    if self.in_range(new_pos) and new_pos not in visited \
                    and self.map[new_pos]-self.map[node.pos]<=1:
                        new_total=node.total+1
                        heapq.heappush(frontier,Node(new_pos,new_total,self.end))
        #print('All nodes explored, no solution found')
        return(float('Inf'))

    def compare_all_paths(self): #Find shortest path out of all potential start points (elevation a)
        return(min([self.find_shortest_path(s) for s in self.map.keys() if chr(self.map[s])=='a']))

class Node(): #Node for A*
    def __init__(self,pos,total,end):
        self.pos=pos
        self.total=total #g in A* algorithm (distance travelled so far)
        self.end=end #End coordinate of cave
        self.h=manhatten_dist(pos,end) #h in A* algorithm (minimum distance to end)
        self.f=self.total+self.h
   
    def __lt__(self, other):
        return(self.f<other.f)

    def __str__(self) -> str:
        return(f'Position={self.pos}, Dist={self.total}, h={self.h}')

def manhatten_dist(a,b): #Return Manhatten distance between two complex coordinates
    return(int(abs(a.real-b.real)+abs(a.imag-b.imag)))

hill=Hill(inp)
print(hill)
print(hill.find_shortest_path())
print(hill.compare_all_paths())