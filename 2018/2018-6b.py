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

def inRange(x0,y0,coords,Rrange):
    sum=0
    for k, v in coords.items():
        d=manDist(x0,y0,v[0],v[1])
        sum+=d
        if sum>=Rrange:
            return(False)
    return(True)
        
coords=importCoords(input)

def find_key(input_dict, value):
    return next((k for k, v in input_dict.items() if v == value), None)

class Spot(): #Position on grid
    
    def __init__(self,x,y,coords,Rrange):
        self.pos=complex(x,y)
        self.region=inRange(x,y,coords,Rrange)


class Grid(): #Grid of coords
    
    def __init__(self,coords,Rrange):
        self.grid={}
        buffer=10 #Area on each side of extremes to check
        self.coords=coords
        self.extremes=coordArea(coords,buffer)
        self.width=self.extremes['maxX']-self.extremes['minX']+1
        self.height=self.extremes['maxY']-self.extremes['minY']+1
        self.regionSize=0
        self.border=set() #If coord is on border, assume it has infinite area
        for i in range(self.extremes['minX'],self.extremes['maxX']+1):
            for j in range(self.extremes['minY'],self.extremes['maxY']+1):
                self.grid[complex(i,j)]=Spot(i,j,coords,Rrange)
                if self.grid[complex(i,j)].region:
                    self.regionSize+=1
                
            
    def __str__(self):
        ret=''
        for j in range(self.extremes['minY'],self.extremes['maxY']):
            for i in range(self.extremes['minX'],self.extremes['maxX']):
                if (i, j) in self.coords.values():
                    ret+=find_key(self.coords, (i, j))
                if self.grid[complex(i,j)].region:
                    ret+='#'
                else:
                    ret+='.'
            ret+='\n'
        return(ret)

#g=Grid(coords,32)
g=Grid(coords,10000)


def solveB(g):
    return(g.regionSize)

retB=solveB(g)
    
    