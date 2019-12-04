#Advent of Code 2018 Day 6

from collections import defaultdict
import re
import string
import copy
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-6.txt')
contents = f.read()
input = contents.splitlines()

def importCoords(input):
    p1=re.compile('(\d+), (\d+)')
    names=string.ascii_letters
    coords={}
    for i in range(len(input)):
        m1=p1.match(input[i])
        coords[names[i]]=(int(m1.group(1)),int(m1.group(2)))
    return(coords)

def coordArea(coords,buffer): #Return min/max x/y values for coord set
    minX=float('Inf')
    minY=float('Inf')
    maxX=0
    maxY=0
    for c in coords.values():
        if c[0]<minX:
            minX=c[0]
        if c[0]>maxX:
            maxX=c[0]
        if c[1]<minY:
            minY=c[1]
        if c[1]>maxY:
            maxY=c[1]
    ret={}
    ret['minX']=minX-buffer
    ret['maxX']=maxX+buffer
    ret['minY']=minY-buffer
    ret['maxY']=maxY+buffer
    return(ret)

def manDist(x0,y0,x1,y1):
    return(abs(x1-x0)+abs(y1-y0))

def minDist(x0,y0,coords):
    nearest=''
    mDist=float('Inf')
    for k, v in coords.items():
        d=manDist(x0,y0,v[0],v[1])
        if d<mDist:
            nearest=k
            mDist=d
        elif d==mDist: #In case of a tie, spot counts for no coord
            nearest='.'
    return((nearest,mDist))

coords=importCoords(input)
m=minDist(3,6,coords)

class Spot(): #Position on grid
    
    def __init__(self,x,y,coords):
        self.pos=complex(x,y)
        m=minDist(x,y,coords)
        self.nearest=m[0] #Nearest named coordinate
        self.nDist=m[1] #Distance to nearest named coordinate

class Grid(): #Grid of coords
    
    def __init__(self,coords):
        self.grid={}
        buffer=10 #Area on each side of extremes to check
        self.extremes=coordArea(coords,buffer)
        self.width=self.extremes['maxX']-self.extremes['minX']+1
        self.height=self.extremes['maxY']-self.extremes['minY']+1
        self.areas=defaultdict(int) #Count area for each named coord
        self.border=set() #If coord is on border, assume it has infinite area
        for i in range(self.extremes['minX'],self.extremes['maxX']+1):
            for j in range(self.extremes['minY'],self.extremes['maxY']+1):
                self.grid[complex(i,j)]=Spot(i,j,coords)
                self.areas[self.grid[complex(i,j)].nearest]+=1 #Add to area count for nearest named coord
                if (i in (self.extremes['minX'],self.extremes['maxX'])) or (j in (self.extremes['minY'],self.extremes['maxY'])):
                    self.border.add(self.grid[complex(i,j)].nearest)
            
    def __str__(self):
        ret=''
        for j in range(self.extremes['minY'],self.extremes['maxY']):
            for i in range(self.extremes['minX'],self.extremes['maxX']):
                ret+=self.grid[complex(i,j)].nearest
            ret+='\n'
        return(ret)

g=Grid(coords)

def solveA(g):
    a=g.areas
    b=list(g.border)
    fin={} #Finite areas
    for k,v in a.items():
        if k not in b:
            fin[k]=v
    maxKey=max(fin,key=fin.get)
    print(str(maxKey))
    return(fin[maxKey])
#6115 too high
retA=solveA(g)
    
    