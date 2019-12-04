#Advent of Code 2016 Day 6

import re
from collections import Counter
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-6.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    
    l=len(input[0])
    letters=['' for x in range(l)]
    message=''
    for each in input:        
        for x in range(l):
            letters[x]+=each[x]
    for x in range(l):
        counts=Counter(letters[x])
        res = sorted(counts.items(), key=lambda kv: -kv[1])
        message+=res[0][0]
    return(message)

retA=solveA(input)

def solveB(input):
    
    l=len(input[0])
    letters=['' for x in range(l)]
    message=''
    for each in input:        
        for x in range(l):
            letters[x]+=each[x]
    for x in range(l):
        counts=Counter(letters[x])
        res = sorted(counts.items(), key=lambda kv: kv[1])
        message+=res[0][0]
    return(message)

retB=solveB(input)