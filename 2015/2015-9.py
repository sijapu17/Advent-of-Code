#Advent of Code 2015 Day 9

import itertools

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-9.txt')
contents = f.read()
input = contents.splitlines()

def distDict(input):
    dists={} #Dictionary of distances
    for each in input: #Set up second layer of ditionary
        loc1=each.split(' ')[0]
        loc2=each.split(' ')[2]
        if loc1 not in dists:
            dists[loc1]={}
        if loc2 not in dists:
            dists[loc2]={}
    for each in input: #Add distances to dictionary in both directions
        loc1=each.split(' ')[0]
        loc2=each.split(' ')[2]
        d=int(each.split(' ')[4])
        dists[loc1][loc2]=d
        dists[loc2][loc1]=d
    return(dists)

dists=distDict(input)

def solveA(dists):
    locs=list(dists.keys())
    routes=list(itertools.permutations(locs))
    minD=float('inf')
    minRt=None
    for r in routes:
        dist=0
        for i in range(len(r)-1):
            dist+=dists[r[i]][r[i+1]]
        if dist<minD:
            minD=dist
            minRt=r
    return(minD)

#retA=solveA(dists)

def solveB(dists):
    locs=list(dists.keys())
    routes=list(itertools.permutations(locs))
    maxD=0
    maxRt=None
    for r in routes:
        dist=0
        for i in range(len(r)-1):
            dist+=dists[r[i]][r[i+1]]
        if dist>maxD:
            maxD=dist
            maxRt=r
    return(maxD)
            

retB=solveB(dists)