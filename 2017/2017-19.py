#Advent of Code 2017 Day 19

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-19.txt')
contents = f.read()
input = contents.splitlines()

class Maze():
    
    def __init__(self,input):
        self.yLen=len(input) #Height of map
        self.xLen=len(input[0]) #Width of map
        self.dirs=(complex(0,-1),complex(-1,0),complex(0,1),complex(1,0))
        self.d=0 #Index of current direction
        self.map={}
        self.letters=''
        self.steps=0
        
        for j in range(self.yLen):
            j1=self.yLen-1-j #Flip y-coordinate as map is read from top to bottom
            for i in range(self.xLen):
                self.map[complex(i,j1)]=input[j][i]

        for i in range(self.xLen): #Find start
            if self.map[complex(i,self.yLen-1)]=='|':
                self.pos=complex(i,self.yLen)
    
    def inBounds(self,coord): #Check whether a coord is in bounds
        if (0<=coord.real<self.xLen and 0<=coord.imag<self.yLen):
            return(True)
        else:
            return(False)
        
    def getContents(self,coord): #Returns content of position on map
        if self.inBounds(coord):
            return(self.map[coord])
        else: #returns ' ' if out of bounds
            return(' ')
    
    def move(self):
        nextPos=self.pos+self.dirs[self.d]
        next=self.getContents(nextPos)
        if (next!=' '): #Move in same direction if possible
            self.pos=self.pos+self.dirs[self.d]
        else: #Try turning left or right if path does not continue forwards
            ld=(self.d-1)%4
            rd=(self.d+1)%4
            lPos=self.pos+self.dirs[ld]
            left=self.getContents(lPos)
            rPos=self.pos+self.dirs[rd]
            right=self.getContents(rPos)
            if (left!=' '):
                self.d=ld #Turn left
                self.pos=self.pos+self.dirs[ld]
            elif (right!=' '):
                self.d=rd #Turn right
                self.pos=self.pos+self.dirs[rd]
            else: #If no path then terminate
                return(self.steps)
        if (self.map[self.pos].isalpha()): #Add letter to collection if found
            self.letters+=next
            print(self.letters)
        self.steps+=1 #Count a step

maze=Maze(input)

def solveB(maze):
    ret=None
    while (ret==None):
        ret=maze.move()
    return(ret)

retB=solveB(maze)
    