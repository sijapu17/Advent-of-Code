#Advent of Code 2017 Day 22

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2017-22.txt')
contents = f.read()
input = contents.splitlines()
#input=['..#','#..','...']

class Grid():
    
    def __init__(self,input):
        self.yLen=len(input) #Height of grid
        self.xLen=len(input[0]) #Width of grid
        self.pos=complex((self.xLen-1)/2,(self.yLen-1)/2) #Start at centre of grid
        self.dirs=(complex(0,-1),complex(-1,0),complex(0,1),complex(1,0))
        self.d=2 #Index of current direction
        self.grid={}
        self.infects=0
        
        for j in range(self.yLen):
            j1=self.yLen-1-j #Flip y-coordinate as grid is read from top to bottom
            for i in range(self.xLen):
                self.grid[complex(i,j1)]=input[j][i]
        
    def getContents(self,coord): #Returns content of position on grid
        if coord not in self.grid:
            self.grid[coord]='.' #Create uninfected node if not previously visited
        return(self.grid[coord])

    def turn(self): #Turn right if current node is infected, else turn left
        if self.grid[self.pos]=='#':
            self.d=(self.d+1)%4
        elif self.grid[self.pos]=='.':
            self.d=(self.d-1)%4            

    def infect(self): #Infect current node if clean, or clean if infected
        if self.grid[self.pos]=='#':
            self.grid[self.pos]='.'
        elif self.grid[self.pos]=='.':
            self.grid[self.pos]='#'
            self.infects+=1 #Count number of infection steps
            
    def move(self): #Move one step in new directions
        nextPos=self.pos+self.dirs[self.d]
        next=self.getContents(nextPos)
        self.pos+=self.dirs[self.d]
        
    def burst(self): #Turn, infect and move
        self.turn()
        self.infect()
        self.move()

grid=Grid(input)

def solveA(grid):
    for i in range(10000):
        if i%500==1:
            print('Step '+str(i))
        grid.burst()
    return(grid.infects)

retA=solveA(grid)