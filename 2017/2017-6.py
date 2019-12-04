# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 20:29:12 2017

@author: Simon
"""

#Advent of Code 2017 Day 6

input=[2,8,8,5,4,2,3,1,5,5,1,2,15,13,5,14]
#input=[0,2,7,0]

def solveA(input):
    bank=input.copy()
    archive=[]
    cycles=0
    ln=len(bank)
    while cycles<100000:
        print("Cycle "+str(cycles))
        print("Bank "+str(bank))
        if bank in archive:
            return(cycles)
        cycles+=1
        archive.append(bank.copy()) #Archive current bank state
        mx=max(bank)
        for i in range(ln):
            if bank[i]==mx:
                j=(i+1)%ln #First bin to distribute to
                valdstb=bank[i] #Value to distribute
                bank[i]=0
                break
        while (valdstb>0):
            bank[j]+=1 #Add one to bin value
            valdstb-=1 
            j=(j+1)%ln #Move to next bin
        
#retA=solveA(input)

def solveB(input):
    bank=input.copy()
    archive={}
    cycles=0
    ln=len(bank)
    bankkey=tuple()
    while cycles<100000:
        print("Cycle "+str(cycles))
        print("Bank "+str(bank))
        if bankkey in archive:
            return(cycles-archive[bankkey])
        archive[bankkey]=cycles #Archive current bank state
        mx=max(bank)
        for i in range(ln):
            if bank[i]==mx:
                j=(i+1)%ln #First bin to distribute to
                valdstb=bank[i] #Value to distribute
                bank[i]=0
                break
        while (valdstb>0):
            bank[j]+=1 #Add one to bin value
            valdstb-=1 
            j=(j+1)%ln #Move to next bin
        cycles+=1        
        bankkey=tuple(bank)
        
retB=solveB(input)