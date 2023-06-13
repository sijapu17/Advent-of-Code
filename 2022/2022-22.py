#Advent of Code 2022 Day 22

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-22.txt')
contents = f.read()
input = contents.splitlines()

class System():
    def __init__(self,input,part) -> None:
        self.part=part #Part 1 or 2 of question
        self.tiles=set() #Non-wall walkable tiles
        self.walls=set()
        self.width=max([len(x) for x in input])
        self.height=len(input)-2
        self.pos=None
        self.dir=complex(1,0) #Start facing right
        for j in range(self.height):
            for i in range(len(input[j])):
                if input[j][i]=='.':
                    self.tiles.add(complex(i,j))
                    if self.pos==None: #Start on topleft-most empty tile
                        self.pos=complex(i,j)
                elif input[j][i]=='#':
                    self.walls.add(complex(i,j))
        #Combine tiles and walls for overall surface
        self.surface=self.tiles.union(self.walls)
        #Parse path instructions
        pathtxt=input[-1].replace('R',',R,').replace('L',',L,').split(',')
        self.path=[int(x) if x.isdigit() else x for x in pathtxt]
        
        #Find all edge tiles in all directions
        self.edges=set()
        for c in self.surface:
            for d in (complex(1,0),complex(-1,0),complex(0,1),complex(0,-1)):
                if c+d not in self.surface:
                    self.edges.add((c,d))

        #Calculate all edge crossings for part 2
        self.crossings={}
        for i in range(50):
            #Pair A
            self.crossings[(complex(100+i,49),complex(0,1))]=(complex(99,50+i),complex(-1,0)) #S->W
            self.crossings[(complex(99,50+i),complex(1,0))]=(complex(100+i,49),complex(0,-1)) #E->N
            #Pair B
            self.crossings[(complex(50+i,149),complex(0,1))]=(complex(49,150+i),complex(-1,0)) #S->W
            self.crossings[(complex(49,150+i),complex(1,0))]=(complex(50+i,149),complex(0,-1)) #E->N
            #Pair C
            self.crossings[(complex(50,50+i),complex(-1,0))]=(complex(0+i,100),complex(0,1)) #W->S
            self.crossings[(complex(0+i,100),complex(0,-1))]=(complex(50,50+i),complex(1,0)) #N->E
            #Pair D
            self.crossings[(complex(149,49-i),complex(1,0))]=(complex(99,100+i),complex(-1,0)) #E->W
            self.crossings[(complex(99,100+i),complex(1,0))]=(complex(149,49-i),complex(-1,0)) #E->W
            #Pair E
            self.crossings[(complex(50,49-i),complex(-1,0))]=(complex(0,100+i),complex(1,0)) #W->E
            self.crossings[(complex(0,100+i),complex(-1,0))]=(complex(50,49-i),complex(1,0)) #W->E
            #Pair F
            self.crossings[(complex(50+i,0),complex(0,-1))]=(complex(0,150+i),complex(1,0)) #N->E
            self.crossings[(complex(0,150+i),complex(-1,0))]=(complex(50+i,0),complex(0,1)) #W->S
            #Pair G
            self.crossings[(complex(100+i,0),complex(0,-1))]=(complex(0+i,199),complex(0,-1)) #N->N
            self.crossings[(complex(0+i,199),complex(0,1))]=(complex(100+i,0),complex(0,1)) #S->S

    def run_path(self): #Run all instructions on path
        for a in self.path:
            self.run_instruction(a)

    def run_instruction(self,instr): #Run given instruction
        #print(self)
        #print(instr)
        if instr=='R':
            self.dir*=complex(0,1) #Multiply by i for clockwise turn
        elif instr=='L':
            self.dir*=complex(0,-1) #Multiply by -i for anticlockwise turn
        else: #Forward movement
            steps=instr
            while steps>0:
                #Find potential next pos and dir
                if (self.pos,self.dir) in self.edges:
                    next_pos,next_dir=self.traverse_border()
                else:
                    next_pos,next_dir=self.pos+self.dir,self.dir
                #Check for wall
                if next_pos in self.walls:
                    steps=0
                    break
                else:
                    self.pos,self.dir=next_pos,next_dir
                    steps-=1


    def traverse_border(self): #Return pos and dir after traversing border (ignoring walls)
        if self.part==1:
            if self.dir==complex(0,-1): #North
                new_pos=max([x[0] for x in self.edges if x[0].real==self.pos.real],key=lambda x:x.imag)
            elif self.dir==complex(0,1): #South
                new_pos=min([x[0] for x in self.edges if x[0].real==self.pos.real],key=lambda x:x.imag) 
            elif self.dir==complex(-1,0): #West
                new_pos=max([x[0] for x in self.edges if x[0].imag==self.pos.imag],key=lambda x:x.real)                                
            elif self.dir==complex(1,0): #East
                new_pos=min([x[0] for x in self.edges if x[0].imag==self.pos.imag],key=lambda x:x.real)  
            return(new_pos,self.dir)
        
        elif self.part==2:
            return(self.crossings[(self.pos,self.dir)])

    def final_password(self): #Calculate final password from row, column and facing
        facing_dict={complex(-1,0):2,complex(1,0):0,complex(0,1):1,complex(0,-1):3}
        row=int(self.pos.imag)+1
        col=int(self.pos.real)+1
        facing=facing_dict[self.dir]
        print(f'Row={row} Col={col} facing={facing}')
        return(1000*row+4*col+facing)

    def __str__(self) -> str:
        ret=''
        dirs={complex(-1,0):'<',complex(1,0):'>',complex(0,1):'V',complex(0,-1):'^'}
        for j in range(self.height):
            for i in range(self.width):
                pos=complex(i,j)
                if pos==self.pos:
                    ret+=dirs[self.dir]
                elif pos in self.tiles:
                    ret+='.'
                elif pos in self.walls:
                    ret+='#'
                else:
                    ret+=' '
            ret+='\n'
        return(ret)        

#system=System(input,1)
#system.run_path()
#print(system)
#print(system.final_password())
system=System(input,2)
system.run_path()
#print(system)
print(system.final_password())