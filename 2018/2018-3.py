#Advent of Code 2018 Day 3

from itertools import product
from collections import defaultdict
import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-3.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    p1=re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    fabric=defaultdict(int)
    dups=0
    for c in input:
        m=p1.match(c)
        i0=int(m.group(2))
        j0=int(m.group(3))
        w=int(m.group(4))
        h=int(m.group(5))
        for i in range(w):
            for j in range(h):
                coord=complex(i0+i,j0+j)
                fabric[coord]+=1
                if fabric[coord]==2:
                    dups+=1
    return(dups)
        
#retA=solveA(input)

def solveB(input):
    p1=re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    fabric=defaultdict(int)
    dups=0
    for c in input:
        m=p1.match(c)
        i0=int(m.group(2))
        j0=int(m.group(3))
        w=int(m.group(4))
        h=int(m.group(5))
        for i in range(w):
            for j in range(h):
                coord=complex(i0+i,j0+j)
                fabric[coord]+=1
                if fabric[coord]==2:
                    dups+=1
    print(str(dups)+' duplicates')
    for c in input:
        unique=True
        m=p1.match(c)
        i0=int(m.group(2))
        j0=int(m.group(3))
        w=int(m.group(4))
        h=int(m.group(5))
        for i,j in product(range(w),range(h)):
            coord=complex(i0+i,j0+j)
            if fabric[coord]>=2:
                unique=False
                break
        if unique:        
            return(m.group(1))

retB=solveB(input)