#Advent of Code 2018 Day 5

import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-5.txt')
input = f.read()

def react(c1,c2): #Check whether two characters react
    if c1.upper()==c2.upper() and c1!=c2:
        return(True)
    return(False)

def solveA(input):
    s=input
    i=0
    while i<len(s)-1:
        if react(s[i],s[i+1]):
            s=s[:i]+s[i+2:]
            i=max(i-1,0)
            #print(len(s))
        else:
            i+=1
    #print(s)
    return(len(s))

#retA=solveA(input)

def solveB(input):
    letters=sorted(''.join(set(input.upper())))
    minLen=float('Inf')
    for l in letters:
        sub=str(l)+'|'+str(l.lower())
        line = re.sub(sub, '', input) #Remove all instances of letter (upper and lower)
        len=solveA(line)
        print(l+': '+str(len))
        if len<minLen:
            minLen=len
    return(minLen)

    

retB=solveB(input)