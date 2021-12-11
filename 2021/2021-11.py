#Advent of Code 2021 Day 11
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-11.txt')
contents = f.read()
inp = contents.splitlines()

class System():
    def __init__(self,inp):
        self.dimX=len(inp[0])
        self.dimY=len(inp)
        self.grid={}
        self.ready_to_flash=[]
        self.flashed_this_step=set()
        self.flashes=0
        self.flash_sync=False
        for y in range(self.dimY):
            for x in range(self.dimX):
                self.grid[complex(x,y)]=int(inp[y][x])

    def __str__(self) -> str:
        ret=''
        for y in range(self.dimY):
            for x in range(self.dimX):
                ret+=str(self.grid[complex(x,y)])
            ret+='\n'
        return(ret)

    def in_range(self,coord): #Check if a coordinate is within the bounds of the system
        return(0<=coord.real<self.dimX and 0<=coord.imag<self.dimY)

    def increase_energy(self): #Increase energy level of each octopus by 1
        for k,v in self.grid.items():
            self.grid[k]+=1
            if self.grid[k]==10:
                self.ready_to_flash.append(k)

    def flash(self,coord): #Flash octopus at coordinate
        self.flashes+=1
        for j in (-1,0,1):
            for i in (-1,0,1):
                neighbour=coord+complex(i,j)
                if neighbour!=coord and self.in_range(neighbour):
                    self.grid[neighbour]+=1
                    if self.grid[neighbour]==10:
                        self.ready_to_flash.append(neighbour)
        self.flashed_this_step.add(coord)

    def reset_flashed(self): #Set value of all octopuses who flashed to 0
        if len(self.flashed_this_step)==self.dimX*self.dimY:
            self.flash_sync=True
        else:
            for coord in self.flashed_this_step:
                self.grid[coord]=0
            self.flashed_this_step=set() #Reset set

    def run_step(self): #Run 1 step of the system
        self.increase_energy()
        while len(self.ready_to_flash)>0:
            coord=self.ready_to_flash.pop()
            self.flash(coord)
        self.reset_flashed()

    def run_n_steps(self,n): #Run n steps of the system
        for x in range(n):
            self.run_step()
        print(f'{self.flashes} total flashes')

    def find_full_sync(self): #Find step where all octopuses first flash
        step=0
        while not self.flash_sync:
            self.run_step()
            step+=1
        print(f'Full sync at step {step}')


system=System(inp)
print(system)
system.run_n_steps(100)
print(system)
system=System(inp)
system.find_full_sync()
print(system)