#Advent of Code 2022 Day 9

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-09.txt')
contents = f.read()
inp = contents.splitlines()

def sign(n):
    return(1 if n>0 else -1 if n<0 else 0)

def non_adjacent(v): #Determine whether vector v is more than 1 orthogonal/diagonal step
    return(max(abs(v.real),abs(v.imag))>1)

class System():
    def __init__(self,inp,size) -> None:
        self.inp=inp
        self.size=size
        self.rope=[complex(0,0)]*size
        self.t_visited=set([complex(0,0)])
        self.dirs={'L':complex(-1,0),'R':complex(1,0),'U':complex(0,1),'D':complex(0,-1)}

    def __str__(self) -> str:
        ret=''
        for j in reversed(range(6)):
            for i in range(6):
                p=complex(i,j)
                if p==self.rope[0]:
                    ret+='H'
                elif p in self.rope:
                    ret+=str(self.rope.index(p))
                elif p==0:
                    ret+='o'
                elif p in self.t_visited:
                    ret+='#'
                else:
                    ret+='.'
            ret+='\n'
        return(ret)
                    
    def run_moves(self): #Simulate all moves
        #print(self)
        for row in self.inp:
            #print(row)
            self.move_head(row)
        return(len(self.t_visited))

    def move_head(self,move): #Move head according to 1 row of movement instruction
        d=self.dirs[move.split()[0]] #Convert direction into complex vector
        n=int(move.split()[1])
        for i in range(n): #Move head 1 step, then move each section to catch up
            self.rope[0]+=d
            for s in range(1,self.size):
                self.move_section(s)
            self.t_visited.add(self.rope[-1])
            #print(self)

    def move_section(self,s): #Move section s after every single square of head movement
        v=self.rope[s-1]-self.rope[s] #Vector of section's position relative to the section in front
        if non_adjacent(v):
            if v.real==0:
                self.rope[s]+=complex(0,sign(v.imag))
            elif v.imag==0:
                self.rope[s]+=complex(sign(v.real),0)
            else:
                self.rope[s]+=complex(sign(v.real),sign(v.imag))

system=System(inp,2)
print(system.run_moves())
system=System(inp,10)
print(system.run_moves())