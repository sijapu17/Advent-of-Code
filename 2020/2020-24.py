#Advent of Code 2020 Day 24

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-24.txt')
state = f.read()
input=state.splitlines()

class Hex(): #Hex coordinate pair with e and ne coords
    def __init__(self,c):

        self.str2tup={'ne':(0,1),'e':(1,0),'se':(1,-1),'sw':(0,-1),'w':(-1,0),'nw':(-1,1)} #Conversion of direction strings to coordinates

        if type(c) is tuple: #Input in form of tuple/list pair
            self.c=c

        elif type(c) is str: #Input in form of str direction
            self.c=self.str2tup[c]

    def __add__(self,other): #Add two Hex objects together
        return(Hex(tuple(map(lambda x, y: x + y,self.c,other.c))))

    def __eq__(self,other): #Test for equality
        return(self.c==other.c)

    def __hash__(self):
        return(hash(self.c))

    def __str__(self):
        return(self.__repr__())

    def __repr__(self):
        return('Hex('+str(self.c)+')')

class Floor():
    def __init__(self,input):
        self.tiles=set()
        self.current=Hex((0,0)) #Origin
        self.instrs=[]
        for l in input:
            self.instrs.append(l.replace('e','e,').replace('w','w,')[:-1].split(','))
        print(self.all_line_ends())

    def move(self,c): #Move one step
        self.current+=Hex(c)

    def follow_line(self,line): #Reset to orgin then follow one line of instructions
        self.current=Hex((0,0)) #Reset to origin
        for x in line:
            self.move(x)

    def all_line_ends(self):
        for i in self.instrs:
            self.follow_line(i)
            c=self.current
            if c in self.tiles: #If tile has already been flipped, flip it back
                self.tiles.remove(c)
            else: #If tile has not been flipped, flip it
                self.tiles.add(c)
        return(self.count_black())

    def update_bounds(self):
        #Find bounds of map
        self.minE=min(self.tiles,key=lambda x:x.c[0]).c[0]
        self.maxE=max(self.tiles,key=lambda x:x.c[0]).c[0]
        self.minNE=min(self.tiles,key=lambda x:x.c[1]).c[1]
        self.maxNE=max(self.tiles,key=lambda x:x.c[1]).c[1]

    def nAdjacent(self,h): #For a given hex, check how many of its 6 neighbours are equal to state
        count=0
        for d in ('ne','e','se','sw','w','nw'):
            nPos=h+Hex(d)
            if nPos in self.tiles: #Do not count cube as its own neighbour                        
                count+=1
        return(count)

    def update(self): #Check adjacent tiles and update each tile
        self.update_bounds() #Update bounds as they will expand over time
        to_add=set() #Tiles that will be added after current state
        to_remove=set() #Tiles that will be removed after current state
        #For each dimension, check from 1 before the min to 1 after the max
        for e in range(self.minE-1,self.maxE+2):
            for ne in range(self.minNE-1,self.maxNE+2):
                pos=Hex((e,ne))
                if pos in self.tiles:
                    if self.nAdjacent(pos) not in (1,2):
                        to_remove.add(pos)
                else:
                    if self.nAdjacent(pos)==2:
                        to_add.add(pos)

        self.tiles-=to_remove
        self.tiles|=to_add

    def update_n_times(self,n):
        for x in range(n):
            if x%10==1:
                print('Step '+str(x))
            self.update()

    def count_black(self): #Return number of black
        return(len(self.tiles))

floor=Floor(input)
floor.update_n_times(100)
print(floor.count_black())