#Advent of Code 2018 Day 25

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-25.txt')
input = f.read().splitlines()

class Point():
    def __init__(self,coords):
        self.coords=coords
        
    def mDist(self,other):
        dist=0
        for i in range(len(self.coords)):
            dist+=abs(self.coords[i]-other.coords[i])
        return(dist)
    
    def inRange(self,other):
        return(self.mDist(other)<=3)
    
    def __str__(self):
        return('P '+str(self.coords))
    
    def __repr__(self):
        return(self.__str__())

def parse(input):
    points=set()
    for p in input:
        coords=[int(a) for a in p.split(',')]
        points.add(Point(coords))
    return(points)

points=parse(input)

def solveA(points):
    constellations={}
    nextID=0
    for p in points:
        IDsInRange=set() #Constellations in range of new point
        for ck,cv in constellations.items():
            for pt in cv:
                if p.inRange(pt):
                    IDsInRange.add(ck)
                    break
        #print(str(p)+': '+str(IDsInRange))
        if len(IDsInRange)==0: #If point is in range of no constellations, make a new constellation
            constellations[nextID]=set([p])
            nextID+=1
        elif len(IDsInRange)>=1: #If point is in range of one constellation, add it
            cID=IDsInRange.pop()
            constellations[cID].add(p)
            while len(IDsInRange)>0: #If point is in range of multiple constellations, merge them
                rID=IDsInRange.pop()
                #print('Before: '+str(constellations[cID]))
                constellations[cID].update(constellations[rID])
                #print('After: '+str(constellations[cID]))
                del constellations[rID]
    #return(len(constellations))
    print(len(constellations))
    return(constellations)
            
            
retA=solveA(points) #640 too high