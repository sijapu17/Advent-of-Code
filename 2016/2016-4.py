#Advent of Code 2016 Day 4

import re
from collections import Counter
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-4.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    
    sum=0
    rooms=[]
    p=re.compile('((^.*)-(\d+))\[(\w+)\]$')
    for each in input:        
        m=p.match(each)
        name=m.group(2)
        name=''.join( c for c in name if  c not in '-' )
        counts=Counter(name)
        res = sorted(counts.items(), key=lambda kv: (-kv[1],kv[0]))
        checkres=''.join([k[0] for k in res[:5]]) #5 Most common characters, tiebreaker of alpha order
        id=int(m.group(3))
        checksum=m.group(4)
        if checkres==checksum:
            sum+=id
            rooms.append(m.group(1))
        
    return(rooms)

retA=solveA(input)

from string import ascii_lowercase as ALPHABET

def shift(message, offset):
    off=offset%len(ALPHABET)
    trans = str.maketrans(ALPHABET, ALPHABET[off:] + ALPHABET[:off])
    return message.lower().translate(trans)

def solveB(input):
    
    rooms=[]
    p=re.compile('(^.*)-(\d+)$')
    for each in input:        
        m=p.match(each)
        name=m.group(1)
        id=int(m.group(2))
        decoded=shift(name,id)
        if decoded=='northpole-object-storage':
            return(id)
        #rooms.append(decoded)
        
    #return(rooms)

retB=solveB(retA)