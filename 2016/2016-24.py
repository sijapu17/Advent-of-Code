#Advent of Code 2016 Day 24

import math
from collections import deque, defaultdict
import string
from itertools import permutations

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-24.txt')
contents = f.read()
input=contents.splitlines()

class HVAC():
        
    def __init__(self,input): #Convert input into map and units
        self.map={}
        self.c2p={} #Dict of coords to point
        self.p2c={} #Dict of point to coord
        self.w=len(input[0])
        self.h=len(input)
        
        for j in range(self.h):
            for i in range(self.w):
                x=input[j][i]
                pos=complex(i,j)
                if x in string.digits:
                    self.c2p[pos]=int(x)
                    self.p2c[int(x)]=pos                    
                self.map[pos]=x
                
        self.pStr=''.join(sorted([str(x) for x in self.p2c.keys()]))
        self.maxID=max([x for x in self.p2c.keys()])
        
        self.calculateDistances()
        self.getRoutes()

    def __str__(self):
        ret1='  '
        ret2='  '
        ret3=''
        for i in range(self.w):
            if i%10==0: #Create tens row at top
                ret1+=str(math.floor(abs(i)/10%10))
            else:
                ret1+=' '
            ret2+=str(abs(i)%10) #Create units row at top
        for j in range(self.h):
            if j%10==0:
                ret3+=str(math.floor(abs(j)/10%10)) #Create tens column going down
            else:
                ret3+=' '
            ret3+=str(abs(j)%10) #Create units column going down
            for i in range(self.w):
                pos=complex(i,j)
                ret3+=self.map[pos]
            ret3+='\n'
        return(ret1+'\n'+ret2+'\n'+ret3)
    
    def calculateDistances(self): #Create dict of distances between each point using BFS
        self.dists=defaultdict(lambda: dict())
        orthog=[complex(0,-1),complex(-1,0),complex(1,0),complex(0,1)]
        for sID in range(len(self.pStr)-1):
            #print('sID='+str(sID))
            toFind=set(range(sID+1,self.maxID+1))
            #print(toFind)
            dests=[v for k,v in self.p2c.items() if k in toFind]
            #print(dests)
            sPos=self.p2c[sID]
            sNode={'pos':sPos,'len':0}
            closed=set()
            open=deque([sNode])
            while len(open)>0 and len(toFind)>0:
                node=open.pop()
                newLen=node['len']+1
                if node['pos'] in dests:
                    foundID=self.c2p[node['pos']]
                    #print(str(foundID)+' '+str(node))
                    self.dists[sID][foundID]=node['len']
                    self.dists[foundID][sID]=node['len']
                    toFind.remove(foundID)
                for o in orthog:
                    newPos=node['pos']+o
                    if self.map[newPos]!='#': #If new position is unoccupied and unvisited, add to end of queue
                        if newPos not in closed:
                            closed.add(newPos)
                            newNode={'pos':newPos,'len':newLen}
                            open.appendleft(newNode)
                            
    def getRoutes(self):
        ret=[]
        p=permutations(range(1,self.maxID+1))
        for r in p:
            #ret.append([0]+list(r)) Part A
            ret.append([0]+list(r)+[0])
        self.routes=ret
        
    def routeDist(self,route):
        d=0
        #print(route)
        for i in range(len(route)-1):
            d+=self.dists[route[i]][route[i+1]]
            #print(str(self.dists[i]))
            #print(str(d))
        return(d)
    
    def shortestRoute(self):
        #for x in self.routes:
            #print(str(x)+' '+str(self.routeDist(x)))
        return(min([self.routeDist(x) for x in self.routes]))
            
hvac=HVAC(input)
retB=hvac.shortestRoute()