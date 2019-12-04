#Advent of Code 2016 Day 8

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-8.txt')
contents = f.read()
input = contents.splitlines()

class Lights(): #Grid of 1000x1000 lights
    
    def __init__(self):
        self.grid={}
        self.width=50
        self.height=6
        for i in range(self.width):
            for j in range(self.height):
                self.grid[complex(i,j)]=0
            
    def nLit(self): #Number of lit lights
        return(sum(self.grid.values()))
    
    def turnOn(self,i,j):
        self.grid[complex(i,j)]=1
            
    def rect(self,imax,jmax):
        for i in range(imax):
            for j in range(jmax):
                self.turnOn(i,j)
                
    def rotRow(self,row,m):
        status=[]
        for i in range(self.width):
            status.append(self.grid[complex(i,row)])
        newstatus=status[-m:]+status[:-m]
        for i in range(self.width):
            self.grid[complex(i,row)]=newstatus[i]
 
    def rotCol(self,col,m):
        status=[]
        for j in range(self.height):
            status.append(self.grid[complex(col,j)])
        newstatus=status[-m:]+status[:-m]
        for j in range(self.height):
            self.grid[complex(col,j)]=newstatus[j]
            
    def __str__(self):
        ret=''
        for j in range(self.height):
            for i in range(self.width):
                if self.grid[complex(i,j)]==1:
                    ret+='@'
                elif self.grid[complex(i,j)]==0:
                    ret+='.'
            ret+='\n'
        return(ret)
                    
            
def solveA(input):
    lights=Lights()
    n=1
    for instr in input:
        print(n)
        if instr.split(' ')[0]=='rect':
            i=int(instr.split(' ')[1].split('x')[0])
            j=int(instr.split(' ')[1].split('x')[1])
            lights.rect(i,j)
        elif instr.split('=')[0]=='rotate row y':
            row=int(instr.split('=')[1].split(' ')[0])
            m=int(instr.split('=')[1].split(' ')[2])
            lights.rotRow(row,m)
        elif instr.split('=')[0]=='rotate column x':
            col=int(instr.split('=')[1].split(' ')[0])
            m=int(instr.split('=')[1].split(' ')[2])
            lights.rotCol(col,m)
        n+=1
    print(lights)
    return(lights.nLit())

#in0=['turn on 0,0 through 1,1']
retA=solveA(input)


            