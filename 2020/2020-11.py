#Advent of Code 2020 Day 11


f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-11.txt')
state = f.read()
input=state.splitlines()

class Seats():
    def __init__(self,input):
        self.map={}
        j=0
        for row in input:
            i=0
            for g in row:
                pos=complex(i,j)
                if g=='#': #Switch to a letter so uppercase/lowercase can be used during update procedure
                    self.map[pos]='X'
                else:
                    self.map[pos]=g
                i+=1
            j+=1
                
        #Find bounds of map
        self.minX=int(min(self.map.keys(),key=lambda x:x.real).real)
        self.maxX=int(max(self.map.keys(),key=lambda x:x.real).real)
        self.minY=int(min(self.map.keys(),key=lambda x:x.imag).imag)
        self.maxY=int(max(self.map.keys(),key=lambda x:x.imag).imag)

        self.stable=False #This will be changed to true once stable state is reached

    def nTotal(self,state): #Count how many seats are equal to state
        count=0
        for v in self.map.values():
            if v==state:
                count+=1
        return(count)

    def nAdjacent(self,pos,state): #For a given position, check how many of its 8 neighbours are equal to state
        count=0
        for i in (-1,0,1):
            for j in (-1j,0,1j):
                if i!=j: #Do not count seat as its own neighbour
                    nPos=pos+i+j
                    if nPos in self.map.keys():
                        if self.map[nPos].upper()==state:
                            count+=1
        return(count)

    def nVisible(self,pos,state): #For a given position, check how many of its 8 visible neighbours are equal to state
        count=0
        for i in (-1,0,1):
            for j in (-1j,0,1j):
                if i!=j: #Do not count seat as its own neighbour
                    dir=i+j
                    nPos=pos+dir
                    while nPos in self.map.keys() and self.map[nPos]=='.': #If neighbour is floor, extend in the same direction until a chair (or edge) is reached
                        nPos+=dir
                    if nPos in self.map.keys():
                        if self.map[nPos].upper()==state:
                            count+=1
        return(count)

    def __str__(self): #Print map
        ret=''
        for j in range(self.minY,self.maxY+1):
            for i in range(self.minX,self.maxX+1):
                pos=complex(i,j)
                symbol=self.map[pos]
                ret+=symbol
            ret+='\n'
        return(ret)

    def updateA(self): #Check adjacent seats and update each seat
        for k,v in self.map.items():
            #Mark seats to be changed as lowercase of their original state, so all changes can be made simultaneously
            if v=='L': #If empty seat has no adjacent occupied seats, it becomes occupied
                if self.nAdjacent(k,'X')==0:
                    self.map[k]='l'
            elif v=='X': #If occupied seat has >=4 adjacent occupied seats, it becomes empty
                if self.nAdjacent(k,'X')>=4:
                    self.map[k]='x'
        #print(self.__str__())
        changes={'x':'L','l':'X'}
        nChanges=0
        for k,v in self.map.items():
            if v in changes:
                self.map[k]=changes[v]
                nChanges+=1
        if nChanges==0:
            self.stable=True

    def updateB(self): #Check visible seats and update each seat
        for k,v in self.map.items():
            #Mark seats to be changed as lowercase of their original state, so all changes can be made simultaneously
            if v=='L': #If empty seat has no adjacent occupied seats, it becomes occupied
                if self.nVisible(k,'X')==0:
                    self.map[k]='l'
            elif v=='X': #If occupied seat has >=5 adjacent occupied seats, it becomes empty
                if self.nVisible(k,'X')>=5:
                    self.map[k]='x'
        #print(self.__str__())
        changes={'x':'L','l':'X'}
        nChanges=0
        for k,v in self.map.items():
            if v in changes:
                self.map[k]=changes[v]
                nChanges+=1
        if nChanges==0:
            self.stable=True

    def findStableA(self): #Update until stable state is reached
        while not self.stable:
            self.updateA()
        return(self.nTotal('X'))

    def findStableB(self): #Update until stable state is reached
        while not self.stable:
            self.updateB()
        return(self.nTotal('X'))

seats=Seats(input)
print(seats.findStableA())       
print(seats.findStableB())