#Advent of Code 2021 Day 15

import heapq, time
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-15.txt')
contents = f.read()
inp = contents.splitlines()

class Cave():

    def __init__(self,inp,size):
        self.map={}
        self.dimX=len(inp[0])
        self.dimY=len(inp)
        self.size=size #Number of times cave map repeats (1 for part 1, 5 for part 2)
        self.end=complex(self.dimX*size-1,self.dimY*size-1)
        self.dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))
        for y in range(self.dimY):
            for x in range(self.dimX):
                for m in range(size):
                    for n in range(size):
                        risk=int(inp[y][x])+m+n
                        if risk>9:
                            risk-=9
                        self.map[complex(x+m*self.dimX,y+n*self.dimY)]=risk

    def __str__(self) -> str:
        ret=''
        for j in range(self.dimY*self.size):
            for i in range(self.dimX*self.size):
                ret+=str(self.map[complex(i,j)])
            ret+='\n'
        return(ret)

    def in_range(self,coord): #Check if a coordinate is within the bounds of the system
        return(0<=coord.real<self.dimX*self.size and 0<=coord.imag<self.dimY*self.size)

    def find_safest_path(self): #Using A* algorithm, find path with the lowest total
        frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
        visited=set() #Visited positions
        start_node=Node(0,0,self.end)
        heapq.heappush(frontier,start_node)
        while len(frontier)>0:
            node=heapq.heappop(frontier) #Examine node in open heap with lowest f
            #print(node)
            if node.pos in visited:
                continue
            if node.pos==self.end: #Check if node is the end node
                print('Solution node found')
                return(node)
            else:
                visited.add(node.pos)
                for d in self.dirs: #Create new node in each direction
                    new_pos=node.pos+d
                    if self.in_range(new_pos) and new_pos not in visited:
                        new_total=node.total+self.map[new_pos]
                        heapq.heappush(frontier,Node(new_pos,new_total,self.end))
        print('All nodes explored, no solution found')


class Node(): #Node for A*
    def __init__(self,pos,total,end):
        self.pos=pos
        self.total=total #g in A* algorithm (total risk so far)
        self.end=end #End coordinate of cave
        self.h=manhatten_dist(pos,end) #h in A* algorithm (minimum risk to end)
        self.f=self.total+self.h
   
    def __lt__(self, other):
        return(self.f<other.f)

    def __str__(self) -> str:
        return(f'Position={self.pos}, Risk={self.total}, h={self.h}')

def manhatten_dist(a,b): #Return Manhatten distance between two complex coordinates
    return(int(abs(a.real-b.real)+abs(a.imag-b.imag)))

start=time.perf_counter() #Test speed of code run
cave=Cave(inp,1)
print(cave.find_safest_path())
mid=time.perf_counter()-start
print(f'Part 1 took {mid} seconds')
cave=Cave(inp,5)
print(cave.find_safest_path())
end=time.perf_counter()-mid
print(f'Part 2 took {end} seconds')