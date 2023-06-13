#Advent of Code 2022 Day 23

from collections import deque, defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-23.txt')
contents = f.read()
input = contents.splitlines()

class Grove():
    def __init__(self,input) -> None:
        #Initial elf positions
        self.elves={}
        n=0
        for j in range(len(input)):
            for i in range(len(input[0])):
                if input[j][i]=='#':
                    self.elves[n]=complex(i,j)
                    n+=1
        self.n_elves=n #Number of elves
        self.update_dimensions()
        #Compass directions
        self.compass={'NW':complex(-1,-1),'N':complex(0,-1),'NE':complex(1,-1),'E':complex(1,0),'SE':complex(1,1),'S':complex(0,1),'SW':complex(-1,1),'W':complex(-1,0)}
        self.dirs=deque(('N','S','W','E'))

    #Check whether elf location has any neighbours in surrounding 8 positions,
    # or in 3 positions around given compass direction
    def has_neighbour(self,pos,compass=None): 
        if compass==None:
            vectors=self.compass.values()
        else: #e.g. compass='N' checks N, NW and NE
            vectors=[x[1] for x in self.compass.items() if compass in x[0]]
        for v in vectors:
            if pos+v in self.elves.values():
                return(True)
        return(False)

    def run_n_rounds(self,n): #Run n rounds of simulation
        for i in range(n):
            self.run_round()
        print(f'{self.n_empty} empty spaces after {n} rounds') 

    def run_until_no_moves(self): #Run rounds until no elf moves in a round
        n=0
        while True:
            n+=1
            m=self.run_round()
            print(f'Round {n}: {m} moves')
            if m==0:
                return(n)


    def run_round(self): #Run 1 round of simulation
        #Part 1: Each elf proposes a move if they have some neighbours but at least one free side
        proposed_moves={}
        pos_count=defaultdict(int)
        for id, pos in self.elves.items():
            if self.has_neighbour(pos): #Elves with no neighbours don't move
                for c in self.dirs:
                    if not self.has_neighbour(pos,c):
                        proposed=pos+self.compass[c]
                        proposed_moves[id]=proposed
                        pos_count[proposed]+=1
                        break

        #Part 2: Elves with proposed moves move if no other elf proposed that position
        successful_moves=0
        for id, pos in proposed_moves.items():
            if pos_count[pos]==1:
                self.elves[id]=pos
                successful_moves+=1

        self.update_dimensions()
        self.dirs.rotate(-1) #Next round, a different direction will be prioritised
        return(successful_moves)

    def update_dimensions(self):    
        #Update grove dimensions
        self.minY=int(min([x.imag for x in self.elves.values()]))
        self.maxY=int(max([x.imag for x in self.elves.values()]))
        self.minX=int(min([x.real for x in self.elves.values()]))
        self.maxX=int(max([x.real for x in self.elves.values()]))
        self.n_empty=(self.maxX-self.minX+1)*(self.maxY-self.minY+1)-self.n_elves

    def __str__(self) -> str:
        ret=''
        for j in range(self.minY,self.maxY+1):
            for i in range(self.minX,self.maxX+1):
                if complex(i,j) in self.elves.values():
                    ret+='#'
                else:
                    ret+='.'
            ret+='\n'
        return(ret)

grove=Grove(input)
#grove.run_n_rounds(10)
grove.run_until_no_moves()