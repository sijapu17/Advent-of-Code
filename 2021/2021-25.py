#Advent of Code 2021 Day 25

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-25.txt')
contents = f.read()
inp = contents.splitlines()

class Sea():
    def __init__(self,inp) -> None:
        self.dimX=len(inp[0])
        self.dimY=len(inp)
        self.east=set() #East-facing squid
        self.south=set() #South-facing squid
        for j in range(self.dimY):
            for i in range(self.dimX):
                val=inp[j][i]
                if val=='>':
                    self.east.add(complex(i,j))
                elif val=='v':
                    self.south.add(complex(i,j))

    def __str__(self) -> str:
        ret=''
        for j in range(self.dimY):
            for i in range(self.dimX):
                pos=complex(i,j)
                if pos in self.east:
                    ret+='>'        
                elif pos in self.south:
                    ret+='v' 
                else:
                    ret+='.'
            ret+='\n'
        return(ret)

    def move_to_halt(self): #Perform steps until no more squid move
        steps=0
        #print(self)
        while True:
            steps+=1
            n_moves=self.move_step()
            print(f'Step {steps}: {n_moves} moves')
            #print(self)
            if n_moves==0:
                print(self)
                return(steps)

    def move_step(self): #Move all squid in either east or south group
        moves=0
        new_pos=set()
        #East-squid moves
        for squid in self.east:
            ahead=squid+complex(1,0) #Try to move squid east
            if ahead.real==self.dimX: #Loop to opposite wall if needed
                ahead=complex(0,ahead.imag)
            if ahead in self.east or ahead in self.south: #If space is occupied, squid stays put
                new_pos.add(squid)
            else: #Else move squid
                new_pos.add(ahead)
                moves+=1
        #Finalise all east-squid moves
        self.east=new_pos
        #South-squid moves
        new_pos=set()
        for squid in self.south:
            ahead=squid+complex(0,1) #Try to move squid south
            if ahead.imag==self.dimY: #Loop to opposite wall if needed
                ahead=complex(ahead.real,0)
            if ahead in self.east or ahead in self.south: #If space is occupied, squid stays put
                new_pos.add(squid)
            else: #Else move squid
                new_pos.add(ahead)
                moves+=1
        #Finalise all south-squid moves
        self.south=new_pos
        return(moves)     

sea=Sea(inp)
print(sea.move_to_halt())    