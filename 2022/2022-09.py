#Advent of Code 2022 Day 9

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-09.txt')
contents = f.read()
inp = contents.splitlines()

def sign(n):
    return(1 if n>0 else -1 if n<0 else 0)

def non_adjacent(v): #Determine whether vector v is more than 1 orthogonal/diagonal step
    return(max(abs(v.real),abs(v.imag))>1)

class System():
    def __init__(self,inp) -> None:
        self.inp=inp
        self.h=complex(0,0) #Position of head
        self.t=complex(0,0) #Position of tail
        self.t_visited=set([complex(0,0)])
        self.dirs={'L':complex(-1,0),'R':complex(1,0),'U':complex(0,1),'D':complex(0,-1)}

    def __str__(self) -> str:
        ret=''
        for j in reversed(range(6)):
            for i in range(6):
                p=complex(i,j)
                match p:
                    case self.h:
                        ret+='H'
                    case self.t:
                        ret+='T'
                    case 0:
                        ret+='o'
                    case _ if p in self.t_visited:
                        ret+='#'
                    case _:
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
        for i in range(n): #Move head 1 step, then move tail to catch up
            self.h+=d
            self.move_tail()
            #print(self)

    def move_tail(self): #Move tail after every single square of head movement
        v=self.h-self.t #Vector of head's position relative to tail
        if non_adjacent(v):
            if v.real==0:
                self.t+=complex(0,sign(v.imag))
            elif v.imag==0:
                self.t+=complex(sign(v.real),0)
            else:
                self.t+=complex(sign(v.real),sign(v.imag))
            self.t_visited.add(self.t)

system=System(inp)
print(system.run_moves())