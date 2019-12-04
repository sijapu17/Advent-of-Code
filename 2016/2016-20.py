#Advent of Code 2016 Day 20

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-20.txt')
input = f.read().splitlines()

def makeRanges(input):
    ranges=[]
    for i in input:
        ranges.append([int(x) for x in i.split('-')])
    out=[]
    sortr=sorted(ranges)
    first=sortr.pop(0)
    low,high=first[0],first[1]
    for r in sorted(ranges):
        if r[0]<=high+1:
            high=max(r[1],high)
        else:
            out.append((low,high))
            low=r[0]
            high=r[1]
    out.append((low,high))      
    return(out)

ranges=makeRanges(input)

def solveA(rIn):
    return(rIn[1][0])

retA=solveA(ranges)

def solveB(rIn):
    maxN=4294967295
    count=0
    for i in range(len(ranges)-1):
        count+=ranges[i+1][0]-ranges[i][1]-1
    count+=max(0,(maxN-ranges[-1][1]))
    return(count)

    return(count)
    
retB=solveB(ranges)