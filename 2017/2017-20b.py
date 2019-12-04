#Advent of Code 2017 Day 20b

import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-20.txt')
contents = f.read()
input = contents.splitlines()

class pList():
    
    def __init__(self,input):
        self.prts={}
        self.step=0
        self.pNum=len(input)
        i=0
        for p in input:
            posStr=re.split('<|>',p)[1].split(',')
            pos=[int(x) for x in posStr]
            velStr=re.split('<|>',p)[3].split(',')
            vel=[int(x) for x in velStr]
            accStr=re.split('<|>',p)[5].split(',')
            acc=[int(x) for x in accStr]
            self.prts[i]=(Particle(pos,vel,acc))
            i+=1
            
    def update(self): #Update all particles
        for p in self.prts:
            self.prts[p].update()
        self.step+=1
            
    def checkCollision(self): #Check for particles in same pos and remove
        posList=[] #Build list of positions
        colList=[] #Add any colliding positions to list
        for p in self.prts:
            ps=self.prts[p].pos
            if ps in posList: #If pos has already been seen on this step, there will be a collision
                colList.append(ps)
            else:
                posList.append(ps)
        newpList={}
        for p in self.prts: #Remove collided particles
            ps=self.prts[p].pos
            if ps not in colList: #Copy particles that dont collide to new dict
                newpList[p]=self.prts[p]
        self.pNum=len(newpList)
        self.prts=newpList
        
                
            
            
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

def solveB(input): #Find number of particles left after collisions
    list=pList(input)
    list.checkCollision()
    for i in range(1000): #Skip early steps
        list.update()
        list.checkCollision()
        if list.step%50==1:
            print('Step '+str(list.step)+' '+str(list.pNum)+' particles')

retB=solveB(input)

            