#Advent of Code 2019 Day 12

import re

from math import gcd
from functools import reduce

def lcm(denominators):
    return reduce(lambda a,b: a*b // gcd(a,b), denominators)

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-12.txt')
contents = f.read()
input=contents.splitlines()

class System(): #System of moons
    def __init__(self):
        self.moons=[]
        
    def __str__(self):
        ret=''
        for m in self.moons:
            ret+='\nPos: '+str(m.pos)+' Vel: '+str(m.vel)
        return(ret[1:]) #Drop first newline
            
    def addMoon(self,moon): #Add moon to system
        self.moons.append(moon)
        
    def getDimStatus(self,d): #Return encoded position and velocity of system in dimension d
        ret=[]
        for m in self.moons:
            ret.append(m.pos[d])
            ret.append(m.vel[d])
        return(tuple(ret))
        
    def applyGravity(self): #For each moon, adjust velocity in each dimension based on relative positions of other moons
        for m in self.moons:
            for d in range(3): #x, y, z dimensions
                for oth in self.moons:
                    if m!=oth:
                        if oth.pos[d]>m.pos[d]: #Increase velocity in direction of each other moon
                            m.vel[d]+=1
                        elif oth.pos[d]<m.pos[d]:
                            m.vel[d]-=1
                            
    def applyVelocity(self): #For each moon, move position in each dimension by value of velocity
        for m in self.moons:
            for d in range(3): #x, y, z dimensions
                m.pos[d]+=m.vel[d]
                
    def applyDimGravity(self,d): #For each moon, adjust velocity in one dimension based on relative positions of other moons
        for m in self.moons:
            for oth in self.moons:
                if m!=oth:
                    if oth.pos[d]>m.pos[d]: #Increase velocity in direction of each other moon
                        m.vel[d]+=1
                    elif oth.pos[d]<m.pos[d]:
                        m.vel[d]-=1
                        
    def applyDimVelocity(self,d): #For each moon, move position in one dimension by value of velocity
        for m in self.moons:
            m.pos[d]+=m.vel[d]                        
                            
    def totalEnergy(self): #Determine total energy in system by multiplying abs sums of pos and vel for each moon
        total=0
        for m in self.moons:
            total+=sum([abs(x) for x in m.pos])*sum([abs(x) for x in m.vel])
        return(total)
            
    def runSteps(self,n): #Run n steps of applying gravity and velocity
        for i in range(n):
            self.applyGravity()
            self.applyVelocity()
            
    def runDimStep(self,d): #Run 1 step of applying gravity and velocity, only in one dimension
        self.applyDimGravity(d)
        self.applyDimVelocity(d)
        
class Moon():
    
    def __init__(self,input):
        p1=re.compile('<x=(.+), y=(.+), z=(.+)>')
        m1=p1.match(input)
        self.pos=[int(m1.group(1)),int(m1.group(2)),int(m1.group(3))]
        self.vel=[0,0,0]
        
def parse(input): #Read in puzzle input
    system=System()
    for i in input:
        system.addMoon(Moon(i))
    return(system)

system=parse(input)

def solveA(system):
    system.runSteps(1000)
    energy=system.totalEnergy()
    print(system)
    return(energy)
    
retA=solveA(system)

system=parse(input)

def solveB(system):
    period=[] #Find number of steps in each dimension for pos and vel to return to origin state
    for d in range(3):
        print('Dimension '+str(d))
        step=0
        status0=system.getDimStatus(d) #Encode origin state for comparison
        print(str(status0))
        while True:
            system.runDimStep(d) #Run simulation in one dimension at a time
            step+=1
            if status0==system.getDimStatus(d):
                period.append(step)
                break
    return(lcm(period)) #Period in 3 dimensions is LCM of the individual periods, as they are independent
        
retB=solveB(system)


