#Advent of Code 2015 Day 13

import itertools

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-13.txt')
contents = f.read()
input = contents.splitlines()

def happDict(input):
    dir={'gain':1,'lose':-1}
    happ={} #Dictionary of happiness
    for each in input: #Set up second layer of dictionary
        name1=each.split(' ')[0]
        name2=each.split(' ')[-1][:-1]
        if name1 not in happ:
            happ[name1]={}
        if name2 not in happ:
            happ[name2]={}
    for each in input: #Add distances to dictionary in both directions
        name1=each.split(' ')[0]
        name2=each.split(' ')[-1][:-1]
        h=int(each.split(' ')[3])*dir[each.split(' ')[2]]
        happ[name1][name2]=h
    return(happ)

happ=happDict(input)

def solveA(happ):
    names=list(happ.keys())
    circles=list(itertools.permutations(names))
    maxH=0
    maxCr=None
    for c in circles:
        h=0
        l=len(c)
        for i in range(l):
            lInd=(i-1)%l
            rInd=(i+1)%l
            h+=happ[c[i]][c[lInd]]+happ[c[i]][c[rInd]]
        if h>maxH:
            maxH=h
            maxCr=c
    return(maxH)

retA=solveA(happ)
            

retA=solveA(happ)