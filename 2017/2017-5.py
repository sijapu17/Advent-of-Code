# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 19:25:24 2017

@author: Simon
"""

#Advent of Code 2017 Day 5

with open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-5.txt') as f:
    a = f.readlines()
    b=[]
    l=len(a)
    a0=int(a[1])
    for i in range(l):
        x=int(a[i])
        b.append(x)

def solveA(input):
    path=input.copy()
    step=1
    pos=0
    l=len(path)
    while step<1000000:
        value=path[pos] #Value of step before incrementing
#        print('Step '+str(step))
#        print('Pos '+str(pos))
#        print('Value '+str(value))
        posold=pos #Position that is being left
        pos=pos+value #Step forward or back according to value
        if (pos<0 or pos>=l): #Check whether position has left bounds
            return(step)
        else:
            path[posold]+=1
            step+=1

#c=[0,3,0,1,-3]
#ret=solveA(b)

def solveB(input):
    path=input.copy()
    step=1
    pos=0
    l=len(path)
    while step<10000000000:
        value=path[pos] #Value of step before incrementing
        if step%10000==0:
            print('Step '+str(step))
#        print('Pos '+str(pos))
#        print('Value '+str(value))
        posold=pos #Position that is being left
        pos=pos+value #Step forward or back according to value
        if (pos<0 or pos>=l): #Check whether position has left bounds
            return(step)
        else:
            if path[posold]>=3:
                path[posold]-=1
            else:
                path[posold]+=1
            step+=1
            
retB=solveB(b)