#Advent of Code 2019 Day 24 Part 2

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-24.txt')
contents = f.read()
input=contents.splitlines()
import math
from collections import defaultdict

class Area():
    def __init__(self,input):
        self.map=defaultdict(lambda : defaultdict(lambda:'.'))
        j=2
        for row in input:
            i=-2
            for g in row:
                pos=complex(i,j)
                self.map[0][pos]=g #Original level is denoted as 0
                i+=1
            j-=1
            
        #Initialise min/max levels
        self.minLevel=0
        self.maxLevel=0
    
    def totalBugs(self): #Count number of bugs in all levels
        count=0
        for lv in range(self.minLevel,self.maxLevel+1):
            count+=sum(v=='#' for v in self.map[lv].values())
        return(count)
    
    def nAdjacent(self,pos,lv):
        count=0
        #Check for adjacent bugs on same level
        for i in (-1,0,1):
            for j in (-1j,0,1j):
                if (i==0 or j==0) and i!=j: #Only count 4 adjacent neighbours
                    nPos=pos+i+j
                    if self.map[lv][nPos]=='#':
                        count+=1
                              
        #Check for adjacent bugs on inner/higher level
        if abs(pos.real)+abs(pos.imag)==1: #Adjacent to inner level if one coord is +/-1 and other is 0
            if pos.real!=0: #Adjacent on left/right side
                i=2*pos.real
                for j in range(-2,3):
                    if self.map[lv+1][complex(i,j)]=='#':
                        count+=1
            elif pos.imag!=0: #Adjacent on top/bottom side
                j=2*pos.imag
                for i in range(-2,3):
                    if self.map[lv+1][complex(i,j)]=='#':
                        count+=1
                        
        #Check for adjacent bugs on outer/lower level
        elif abs(pos.real)==2 or abs(pos.imag)==2: #Adjacent to outer layer if at least one coord is +/-2
            if abs(pos.real)==2: #Adjacent on left/right side
                i=pos.real//2
                if self.map[lv-1][complex(i,0)]=='#':
                    count+=1
            if abs(pos.imag)==2: #Adjacent on top/bottom side
                j=pos.imag//2
                if self.map[lv-1][complex(0,j)]=='#':
                    count+=1
        
        #print('level='+str(lv)+' pos='+str(pos)+' neighbours='+str(count))
        return(count)
                   
       
    
    def update(self): #Check adjacent acres and update each acre
        newItems=defaultdict(lambda : defaultdict(lambda:'.'))
        for lv in range(self.minLevel,self.maxLevel+1):
            for j in range(-2,3):
                for i in range(-2,3):
                    if (i,j)!=(0,0):
                        if self.map[lv][complex(i,j)]=='#':
                            if self.nAdjacent(complex(i,j),lv)==1:
                                newItems[lv][complex(i,j)]='#'
                            else:
                                newItems[lv][complex(i,j)]='.'
                        elif self.map[lv][complex(i,j)]=='.':
                            if self.nAdjacent(complex(i,j),lv) in (1,2):
                                newItems[lv][complex(i,j)]='#'
                            else:
                                newItems[lv][complex(i,j)]='.'
        self.map=newItems
                
    def __str__(self):
        ret=''
        for lv in range(self.minLevel,self.maxLevel+1):
            ret+=('\nDepth '+str(lv)+':\n')
            for j in range(2,-3,-1):
                for i in range(-2,3):
                    pos=complex(i,j)
                    symbol=self.map[lv][pos]
                    if (i,j)==(0,0):
                        symbol='?'
                    ret+=symbol
                ret+='\n'
        return(ret)


def solveB(input,nReps):
    area=Area(input)
    print(area)
    for n in range(nReps):
        if n%2==0: #Expand level boundary every other minute
            area.minLevel-=1
            area.maxLevel+=1
        if n%20==1:
            print('n='+str(n))
        area.update()
    #print(area)
    return(area.totalBugs())

retB=solveB(input,200)