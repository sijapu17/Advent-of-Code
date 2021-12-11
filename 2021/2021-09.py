#Advent of Code 2021 Day 9

import math
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-09.txt')
contents = f.read()
inp = contents.splitlines()

class System():
    def __init__(self,inp):
        self.dimX=len(inp[0])
        self.dimY=len(inp)
        self.grid={}
        self.dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))
        self.lowpoints=[] #List of all lowpoints
        for y in range(self.dimY):
            for x in range(self.dimX):
                self.grid[complex(x,y)]=int(inp[y][x])

    def in_range(self,coord): #Check if a coordinate is within the bounds of the system
        return(0<=coord.real<self.dimX and 0<=coord.imag<self.dimY)

    def sum_risk_levels(self): #Count low points and sum their risk levels
        sum=0
        for coord in self.grid.keys():
            low_flag=True
            for dir in self.dirs:
                neighbour=coord+dir
                if self.in_range(neighbour) and self.grid[coord]>=self.grid[neighbour]:
                    low_flag=False
            if low_flag:
                self.lowpoints.append(coord)
                sum+=1+self.grid[coord] #Add 1 plus coord height to sum if coord is lower than all neighbours
        return(sum)

    def basin_size(self,coord): #Find size of basin around a particular lowpoint using DFS
        frontier=[coord]
        visited=set()
        while len(frontier)>0:
            current=frontier.pop() #Current coordinate to investigate
            visited.add(current)
            for dir in self.dirs: #Add each of the four neighbours to frontier if they are unvisited and not 9 or out of bounds
                neighbour=current+dir
                if self.in_range(neighbour) and self.grid[neighbour]<9 and neighbour not in visited and neighbour not in frontier:
                    frontier.append(neighbour)
        return(len(visited))

    def find_largest_basins(self): #Find size of each basin, and return sum of largest 3
        sizes=[] #List of all basin sizes
        for d in self.lowpoints: #Loop through each lowpoint to find its basin size
            sizes.append(self.basin_size(d))
        sizes.sort()
        return(math.prod(sizes[-3:]))

system=System(inp)
print(system.sum_risk_levels())
print(system.find_largest_basins())