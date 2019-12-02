#Advent of Code 2015 Day 6

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2015-6.txt')
contents = f.read()
input = contents.splitlines()

class Lights(): #Grid of 1000x1000 lights
    
    def __init__(self):
        self.grid={}
        for i in range(1000):
            for j in range(1000):
                self.grid[complex(i,j)]=0
            
    def nLit(self): #Number of lit lights
        return(sum(self.grid.values()))
    
    def turnOn(self,i,j):
        self.grid[complex(i,j)]=1
    
    def turnOff(self,i,j):
        self.grid[complex(i,j)]=0
        
    def toggle(self,i,j):
        self.grid[complex(i,j)]=1-self.grid[complex(i,j)]
        
    def instruct(self,type,i0,i1,j0,j1): #Loop required instruction across rectangular range
        for i in range(i0,i1+1):
            for j in range(j0,j1+1):
                if type=='toggle':
                    self.toggle(i,j)
                elif type=='turnOn':
                    self.turnOn(i,j)
                elif type=='turnOff':
                    self.turnOff(i,j)

def solveA(input):
    lights=Lights()
    n=1
    for instr in input:
        print(n)
        if instr.split(' ')[0]=='toggle':
            type='toggle'
            in1=instr.split(' ')[1:]
        elif instr.split(' ')[1]=='on':
            type='turnOn'
            in1=instr.split(' ')[2:]
        elif instr.split(' ')[1]=='off':
            type='turnOff'
            in1=instr.split(' ')[2:]
        i=in1[0]
        j=in1[2]
        i0=int(i.split(',')[0])
        j0=int(i.split(',')[1])
        i1=int(j.split(',')[0])
        j1=int(j.split(',')[1])
        lights.instruct(type,i0,i1,j0,j1)
        n+=1
#    return(lights)
    return(lights.nLit())

#in0=['turn on 0,0 through 1,1']
retA=solveA(input)


            