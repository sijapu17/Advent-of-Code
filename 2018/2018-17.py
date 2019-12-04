#Advent of Code 2018 Day 17

import sys
sys.setrecursionlimit(300000)
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-17.txt')
contents = f.read()
input=contents.splitlines()
from collections import defaultdict
from collections import deque
import re
import math

def empty(): #Dummy function to return an empty pot when required
    return('.')

def below(pos): #Return position below pos
    return(pos+complex(0,1))

def above(pos): #Return position above pos
    return(pos+complex(0,-1))

def left(pos): #Return position to left of pos
    return(pos+complex(-1,0))

def right(pos): #Return position to right of pos
    return(pos+complex(1,0))

class Ground():
    
    def __init__(self,input):
        self.map=defaultdict(empty)
        self.start=complex(500,0)
        px=re.compile('x=(\d+), y=(\d+)\.\.(\d+)')
        py=re.compile('y=(\d+), x=(\d+)\.\.(\d+)')
        for e in input:
            if px.match(e):
                m=px.match(e)
                x=int(m.group(1))
                y0=int(m.group(2))
                y1=int(m.group(3))
                for j in range(y0,y1+1):
                    self.map[complex(x,j)]='#'
            elif py.match(e):
                m=py.match(e)
                y=int(m.group(1))
                x0=int(m.group(2))
                x1=int(m.group(3))
                for i in range(x0,x1+1):
                    self.map[complex(i,y)]='#'
        #Find bounds of map
        self.minX=int(min(self.map.keys(),key=lambda x:x.real).real)
        self.maxX=int(max(self.map.keys(),key=lambda x:x.real).real)
        self.minY=int(min(self.map.keys(),key=lambda x:x.imag).imag)
        self.maxY=int(max(self.map.keys(),key=lambda x:x.imag).imag)
        
        #Create spring
        self.map[complex(500,0)]='+'
        
    def fillDown(self,sPos): #Fill down from source
        #print('Filling down from '+str(sPos))
        #print(str(complex(501,3))+str(self.map[complex(501,3)]))
        blw=below(sPos)
        if sPos.imag<=self.maxY: #Only fill up to bottom of region
            if self.map[blw]=='.': #If sand below, repeat one space below
                self.map[sPos]='|'
                self.fillDown(blw)
            elif self.map[blw] in set(['#','~']): #If there is a floor below, flow sideways
                self.fillAcross(sPos)
            elif self.map[blw]=='|': #If flowing water below, set to flowing
                self.map[sPos]='|'
        #print('Finishing fill down from '+str(sPos))
        #print(str(complex(501,3))+str(self.map[complex(501,3)]))
                
    def fillAcross(self,sPos): #Fill across from source
        #print('Filling across from '+str(sPos))
        #print(str(complex(501,3))+str(self.map[complex(501,3)]))
        abv=above(sPos)
        flowed=False #Track whether stream has flowed out either side
        self.map[sPos]='|'
        #First flow left
        pos=left(sPos)
        while self.map[pos] not in ('#') and not(self.map[pos]=='|' and self.map[below(pos)]=='|'):
            if self.map[pos] not in ('#','~','|'): #If pos is not a wall
                self.map[pos]='|' #Add flowing water
                #if self.map[below(pos)]=='|': #Settle flowing water below
                #    self.map[below(pos)]='~'
                if self.map[below(pos)] in ('.'): #If sand below, flow down
                    flowed=True
                    self.fillDown(pos)
                    break
            pos=left(pos)
        if self.map[pos]=='#':
            leftWall=pos
        else:
            flowed=True
        #Secondly flow right
        pos=right(sPos)
        while self.map[pos] not in ('#') and not(self.map[pos]=='|' and self.map[below(pos)]=='|'):
            if self.map[pos] not in ('#','~','|'): #If pos is not a wall
                self.map[pos]='|' #Add flowing water
                #if self.map[below(pos)]=='|': #Settle flowing water below
                #    self.map[below(pos)]='~'
                if self.map[below(pos)] in ('.'): #If sand below, flow down
                    flowed=True
                    self.fillDown(pos)
                    break
            pos=right(pos)
        if self.map[pos]=='#':
            rightWall=pos
        else:
            flowed=True
        if not flowed:
            #print('Settling '+str(leftWall)+' to' +str(rightWall))
            pos=right(leftWall) #Settle water between two walls
            while pos!=rightWall:
                self.map[pos]='~'
                pos=right(pos)
            self.fillAcross(abv)
        #print('Finishing fill across from '+str(sPos))
        #print(str(complex(501,3))+str(self.map[complex(501,3)]))
                
    def countWater(self):
        count=0
        for k,v in self.map.items():
            if self.minY<=k.imag<=self.maxY:
                if v in set(['|','~']):
                    count+=1
        return(count)
                
    def countSettled(self):
        count=0
        for k,v in self.map.items():
            if self.minY<=k.imag<=self.maxY:
                if v in set(['~']):
                    count+=1
        return(count)            
    
    def __str__(self):
        ret1='  '
        ret2='  '
        ret3=''
        for i in range(self.minX-2,self.maxX+3):
            if i%10==0: #Create tens row at top
                ret1+=str(math.floor(abs(i)/10%10))
            else:
                ret1+=' '
            ret2+=str(abs(i)%10) #Create units row at top
        for j in range(self.minY,self.maxY+1):
            if j%10==0:
                ret3+=str(math.floor(abs(j)/10%10)) #Create tens column going down
            else:
                ret3+=' '
            ret3+=str(abs(j)%10) #Create units column going down
            for i in range(self.minX-2,self.maxX+3):
                pos=complex(i,j)
                ret3+=self.map[pos]
            ret3+='\n'
        return(ret1+'\n'+ret2+'\n'+ret3)

def solveA(input):
    ground=Ground(input)
    ground.fillDown(ground.start)
    #print(str(complex(501,3))+str(ground.map[complex(501,3)]))
    print(ground)
    return(ground.countWater())

#retA=solveA(input)
#73379 too high - flowing too many times to left
#52758 too low - check y=280
#52820 too high
#52800 correct

def solveB(input):
    ground=Ground(input)
    ground.fillDown(ground.start)
    #print(str(complex(501,3))+str(ground.map[complex(501,3)]))
    print(ground)
    return(ground.countSettled())

retB=solveB(input)