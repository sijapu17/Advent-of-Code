#Advent of Code 2017 Day 20

import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-20.txt')
contents = f.read()
input = contents.splitlines()

class pList():
    
    def __init__(self,input):
        self.prts=[]
        self.step=0
        for p in input:
            posStr=re.split('<|>',p)[1].split(',')
            pos=[int(x) for x in posStr]
            velStr=re.split('<|>',p)[3].split(',')
            vel=[int(x) for x in velStr]
            accStr=re.split('<|>',p)[5].split(',')
            acc=[int(x) for x in accStr]
            self.prts.append(Particle(pos,vel,acc))
            
    def closest(self): #Find closest particle to origin
        min=9999999
        pmin=0 #id number of the closest particle
        i=0
        for p in self.prts:
            dist=p.manDist()
            if dist<min:
                min=dist
                pmin=i
            i+=1
        return(pmin)
    
    def update(self): #Update all particles
        for p in self.prts:
            p.update()
        self.step+=1
            
            
            
class Particle():
    
    def __init__(self,pos,vel,acc):
        self.pos=pos
        self.vel=vel
        self.acc=acc
    
    def manDist(self):
        return(sum([abs(x) for x in self.pos]))
    
    def update(self): #Update velocity and position of particle
        for i in range(3):
            self.vel[i]+=self.acc[i]
            self.pos[i]+=self.vel[i]

def solveA(input): #Find closest in the long term to the origin
    list=pList(input)
    inARow=0 #Check for stable closest particle
    for i in range(500): #Skip early steps
        list.update()
        if list.step%50==1:
            print('Step '+str(list.step))
    prev=list.closest()
    while inARow<100:
        list.update()
        if list.step%50==1:
            print('Step '+str(list.step))
        close=list.closest()
        if close==prev:
            inARow+=1
        else:
            inARow=0
        prev=close
    return(prev)

retA=solveA(input)

            