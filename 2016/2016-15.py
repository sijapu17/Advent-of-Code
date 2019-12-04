#Advent of Code 2016 Day 15

import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-15.txt')
contents = f.read()
input = contents.splitlines()

def getDisks(input):
    disks={}
    p1=re.compile('^Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)\.$')
    for d in input:
        m=p1.match(d)
        disks[int(m.group(1))]=(int(m.group(2)),int(m.group(3)))
    return(disks)
        
disks=getDisks(input)

def diskPos(level,status,startTime): #Return position of disk given start time
    size=status[0]
    return((status[1]+level+startTime)%size)

def isSafe(disks,delay): #Check whether ball will pass through disks, with delay
    for level, status in disks.items():
        if diskPos(level,status,delay)!=0:
            return(False)
    return(True)

def solveA(disks):
    d=0 #Start with zero delay, increment to find a safe path
    while True:
        if isSafe(disks,d):
            return(d)
        d+=1
        
retA=solveA(disks)
disks[7]=(11,0)
retB=solveA(disks)
