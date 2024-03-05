#Advent of Code 2023 Day 22

import re
from collections import OrderedDict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-22.txt')
contents = f.read()
input = contents.splitlines()

p1=re.compile("(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")

class Brick():
    def __init__(self,id:int,dims:str) -> None:
        self.id=id
        m=p1.match(dims)
        self.x=(int(m.group(1)),int(m.group(4)))
        self.y=(int(m.group(2)),int(m.group(5)))
        self.z=[int(m.group(3)),int(m.group(6))]
        self.others_above=set()
        self.others_below=set()
        self.resting_on=set() #Set of other bricks that this brick is resting on


    def overlaps(self,other): #Test whether two bricks overlap (from a top-down perspective)
       return(self.x[0]<=other.x[1] and other.x[0]<=self.x[1] and self.y[0]<=other.y[1] and other.y[0]<=self.y[1]) 

    def is_resting_on(self,other): #Test whether brick is resting on an overlapping brick
        return(self.overlaps(other) and self.z[0]-other.z[1]==1)
    
    def max_z_below(self): #Find highest z value below brick
        if len(self.others_below)>0:
            return(max([b.z[1] for id, b in bricks.items() if id in self.others_below]))
        return(0)
        
    def drop(self): #Drop brick as far as possible
        dist=self.z[0]-self.max_z_below()-1 #Distance to drop
        self.z=[a-dist for a in self.z]

    def __str__(self):
        disp=lambda a: a[0] if a[0]==a[1] else a
        return(f'B([{self.id}]:x={disp(self.x)},y={disp(self.y)},z={disp(self.z)})')

    def __repr__(self) -> str:
        return(self.__str__())
    
#Create dict of bricks
bricks={}
for i in range(len(input)):
    bricks[i]=Brick(i,input[i])

#For each brick, work out which other bricks overlap above and below (populate others_below and others_above)
for i in range(len(input)):
    for j in range(i+1,len(input)):
        if bricks[i].overlaps(bricks[j]):
            if bricks[i].z[0]<bricks[j].z[0]: #Case where brick i is lower
                bricks[i].others_above.add(j)
                bricks[j].others_below.add(i)
            else: #Case where brick j is lower
                bricks[i].others_below.add(j)
                bricks[j].others_above.add(i)

#Sort bricks by z[0] and drop them until they reach the ground or the highest brick below them
bricks=OrderedDict(sorted(bricks.items(),key=lambda x:x[1].z[0]))
for b in bricks.values():
    b.drop()
    if b.z[0]==1: #Block resting on ground
        b.resting_on.add('G')
#For each brick, check if there are any other bricks solely supported by it
cannot_disintegrate=set()

for b in bricks.values():
    b_resting_on=[]
    for o in bricks.values():
        if b.is_resting_on(o):
            b.resting_on.add(o.id)
            b_resting_on.append(o.id)
    if len(b_resting_on)==1: #Cannot disintegrate brick o if brick b is solely resting on it
        cannot_disintegrate.add(b_resting_on.pop())

print(len(bricks)-len(cannot_disintegrate))

#For each brick, determine how many other bricks would fall
def how_many_fall(id):
    fallen=set()
    to_fall=set()
    to_fall.add(id)
    while len(to_fall)>0:
        fallen|=to_fall
        to_fall=set()
        for id_o, b_o in bricks.items():
            if id_o not in fallen and b_o.resting_on.issubset(fallen):
                to_fall.add(id_o)
    return(len(fallen)-1)

count=0
for i in bricks.keys():
    count+=how_many_fall(i)
print(count)
