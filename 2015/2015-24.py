#Advent of Code 2015 Day 24

from itertools import combinations
from operator import mul
from functools import reduce
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-24.txt')
contents = f.read()
input = contents.splitlines()
packages=[int(x) for x in input]
packages.reverse()

def solveA(input):

    cptWght=int(sum(input)/3) #Weight required for each compartment
    solved=False
    n=1
    while True:
        print(str(n)+' items')
        good=[x for x in list(combinations(input,n)) if sum(x)==cptWght]
        if len(good)>0:
            break
        n+=1
    
    smallest=min(good,key=lambda x:reduce(mul,x))
    print(str(smallest))
    return(reduce(mul,smallest))
        
#retA=solveA(packages)

def solveB(input):

    cptWght=int(sum(input)/4) #Weight required for each compartment
    solved=False
    n=1
    while True:
        print(str(n)+' items')
        good=[x for x in list(combinations(input,n)) if sum(x)==cptWght]
        if len(good)>0:
            break
        n+=1
    
    smallest=min(good,key=lambda x:reduce(mul,x))
    print(str(smallest))
    return(reduce(mul,smallest))

retB=solveB(packages)
