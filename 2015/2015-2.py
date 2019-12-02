#Advent of Code 2015 Day 2

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2015-2.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    insort=[]
    paper=0
    for i in input:
        i1=sorted([int(y) for y in i.split('x')])
        paper+=3*i1[0]*i1[1]+2*i1[0]*i1[2]+2*i1[1]*i1[2]
    return(paper)

#retA=solveA(input)

def solveB(input):
    insort=[]
    ribbon=0
    for i in input:
        i1=sorted([int(y) for y in i.split('x')])
        ribbon+=2*i1[0]+2*i1[1]+i1[0]*i1[1]*i1[2]
    return(ribbon)

retB=solveB(input)