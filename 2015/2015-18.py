#Advent of Code 2015 Day 18

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2015-18.txt')
contents = f.read()
input = contents.splitlines()

class Lights(): #Grid of 100x100 lights
    
    def __init__(self,Input):
        self.grid={}
        for i in range(100):
            for j in range(100):
                if Input[j][i]=='#':
                    state=1
                else:
                    state=0
                self.grid[complex(i,j)]=state
            
    def nLit(self): #Number of lit lights
        return(sum(self.grid.values()))
    
    def getState(self,C): #Return state of light at coordinate C
        if min(C.real,C.imag)<0 or max(C.real,C.imag)>99: #Return 0 for checks outside the light grid
            return(0)
        else:
            return(self.grid[C])
        
    def nebGrid(self): #Generate grid of neighbour numbers
        self.nGrid={}
        for c in self.grid:
            numNeb=-self.getState(c) #Account for counting current light as its own neighbour
            for h in [-1,0,1]:
                for v in [-1j,0j,1j]:
                    numNeb+=self.getState(c+h+v)
            self.nGrid[c]=numNeb

    
    def update(self): #Update light state by checking neighbours and turning each light on or off
        self.nebGrid() #Generate grid of neighbour numbers
        for c in self.grid:
            if self.grid[c]==1:
                if not 2<=self.nGrid[c]<=3:
                    self.grid[c]=0
            elif self.grid[c]==0:
                if self.nGrid[c]==3:
                    self.grid[c]=1
                
    
    def turnOff(self,i,j):
        self.grid[complex(i,j)]=0

def solveA(Input,nreps):
    lights=Lights(Input)
    for i in range(nreps): #Update nreps times
        print('Step '+str(i))
        lights.update()
    return(lights.nLit())

#retA=solveA(input,100)

def solveB(Input,nreps):
    lights=Lights(Input)
    for i in range(nreps): #Update nreps times
        print('Step '+str(i))
        lights.update()
        for c in [0,99,99j,99+99j]: #Corner lights are stuck on
            lights.grid[c]=1
    return(lights.nLit())

retB=solveB(input,100)