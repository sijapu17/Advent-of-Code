# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 10:09:38 2017

@author: Simon
"""

#Advent of Code 2017 Day 4

with open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-4.txt') as f:
    a = f.readlines()
    
input=a

def solveA(input):
    total=0
    for line in input:
        words=line.split()
        words.sort()
        ln=len(words)
        val=1 #Start value at 1, reduce to 0 if a match is found
        for i in range(ln-1):
            if words[i]==words[i+1]:
                val=0
        total+=val
    return(total)
    
#retA=solveA(input)

def solveB(input):
    total=0
    for line in input:
        words=line.split()
        words1=[]
        for w in words:
            words1.append(''.join(sorted(w)))
        words1.sort()
        ln=len(words1)
        val=1 #Start value at 1, reduce to 0 if a match is found
        for i in range(ln-1):
            if words1[i]==words1[i+1]:
                val=0
        total+=val
    return(total)
    
retB=solveB(input)