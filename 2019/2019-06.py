#Advent of Code 2019 Day 6

from collections import deque

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-06.txt')
contents = f.read()
input = [x.split(')') for x in contents.splitlines()]

def makeOrbitDict(input):
    orbits=dict() #Dict of dicts containing each planet, their orbit level and their children
    toAdd=deque() #Planets in queue to be processed
    toAdd.append(['COM','',0]) #Name, parent, orbit level

    while len(toAdd)>0:
        #Pop current node from queue and extract data (name, parent, level)
        current=toAdd.pop()
        name=current[0]
        parent=current[1]
        level=current[2] #Orbit level, starting at 0 for COM
        #Find all children of current planet
        children=[]
        for pair in input:
            if pair[0]==name:
                children.append(pair[1])
                toAdd.append([pair[1],name,level+1])
        #Create current planet's entry in dictionary
        planet={}
        planet['children']=children
        planet['parent']=parent
        planet['level']=level
        orbits[name]=planet
                
    return(orbits)

orbits=makeOrbitDict(input)

def countOrbits(orbits):
    ret=sum([v['level'] for v in orbits.values()])
    return(ret)

#retA=countOrbits(orbits)

def listAncestors(orbits,planet): #List a planet's ancestors (in order) so the common ancestor can be found
    ret=[]
    current=planet
    while current!='COM':
        current=orbits[current]['parent']
        ret.append(current)
    return(ret)

def commonAncestor(orbits,p0,p1): #Find nearest common ancestor between p0 and p1
    l0=listAncestors(orbits,p0)
    l1=listAncestors(orbits,p1)
    for l in l0:
        if l in l1:
            return(l)

def shortestPath(orbits,p0,p1): #Shortest path between p0 and p1
    common=commonAncestor(orbits,p0,p1)
    #Shortest path is distance from each planet to origin, minus distance from common to origin
    return(orbits[p0]['level']+orbits[p1]['level']-2*orbits[common]['level'])
        
retB=shortestPath(orbits,'YOU','SAN')-2 #Minus 2 as we want the distance between the parent planets of YOU and SAN 