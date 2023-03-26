#Advent of Code 2022 Day 14
import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-14.txt')
contents = f.read()
inp = contents.splitlines()

def sign(n):
    return(1 if n>0 else -1 if n<0 else 0)

class Cave():
    def __init__(self,inp,part) -> None:
        self.rocks=set() #Positions of rock
        self.sand=set() #Positions of settled sand
        self.source=complex(500,0)
        self.part=part #Part 1 or 2

        for line in inp:
            text_coords=re.findall(r"\d*,\d*", line)
            coords=[]
            for t in text_coords:
                coords.append(complex(int(t.split(',')[0]),int(t.split(',')[1])))
            pos=coords[0]
            self.rocks.add(pos)
            for c in coords[1:]: #Trace line of rocks between coordinates
                v=c-pos
                dir=complex(sign(v.real),sign(v.imag))
                while pos!=c:
                    pos+=dir
                    self.rocks.add(pos)
        self.minY=int(self.source.imag) #Highest level (source)
        self.maxY=int(max([x.imag for x in self.rocks])) #Lowest rock level
        self.minX=int(min([x.real for x in self.rocks]))
        self.maxX=int(max([x.real for x in self.rocks]))
        self.abyss=False #Indicator for sand falling into abyss
        self.floorY=self.maxY+2


    def __str__(self) -> str:
        ret=''
        if len(self.sand)==0:
            l=self.minX
            r=self.maxX
        else:
            l=int(min(self.minX,min([x.real for x in self.sand])))
            r=int(max(self.maxX,max([x.real for x in self.sand])))
        for j in range(self.minY,self.floorY+1):
            for i in range(l,r+1):
                c=complex(i,j)
                if c==self.source:
                    ret+='+'
                elif c in self.rocks:
                    ret+='#'
                elif c in self.sand:
                    ret+='o'
                elif j==self.floorY:
                    ret+='F'
                else:
                    ret+='.'
            ret+='\n'
        return(ret)
    
    def is_empty(self,c:complex):
        return(c not in self.rocks and c not in self.sand)

    def drop_1_sand(self): #Drop one unit of sand, recording where it settles
        pos=self.source
        settled=False
        while not settled:
            if pos.imag==self.floorY: #Detect if sand is dropping into abyss
                self.abyss=True
                return()
            settled=True #Temporarily set to true while looking for next move
            if self.part==2 and pos.imag==self.maxY+1:
                break #For part 2 only, settle sand on floor
            for v in [complex(0,1),complex(-1,1),complex(1,1)]:
                if self.is_empty(pos+v):
                    pos+=v
                    settled=False
                    break
        self.sand.add(pos)
    
    #Drop units of sand until it reaches abyss (part 1) or covers source (part 2)
    def drop_until_abyss(self):
        while not self.abyss and self.source not in self.sand:
            self.drop_1_sand()
        print(f'{len(self.sand)} units of sand at rest')
            
cave=Cave(inp,1)
cave.drop_until_abyss()
print(cave)
cave=Cave(inp,2)
cave.drop_until_abyss()
print(cave) #644 too low