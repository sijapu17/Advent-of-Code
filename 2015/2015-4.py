#Advent of Code 2015 Day 4

import hashlib

input='iwrupvqb'

def solveA(input):
    i=1
    while True:
        if i%10000==1:
            print('Step '+str(i))
        instr=input+str(i)
        m=hashlib.md5(instr.encode()).hexdigest()
        if m[:5]=='00000':
            return(i)
        i+=1
        
retA=solveA(input)

def solveB(input):
    i=retA
    while True:
        if i%100000==1:
            print('Step '+str(i))
        instr=input+str(i)
        m=hashlib.md5(instr.encode()).hexdigest()
        if m[:6]=='000000':
            return(i)
        i+=1
        
retB=solveB(input)