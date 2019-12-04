#Advent of Code 2016 Day 3

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-3.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    
    count=0
    
    for each in input:
        sides=[int(x) for x in each.lstrip().split()]
        sides=sorted(sides)
        if sides[0]+sides[1]>sides[2]:
            count+=1
    return(count)

#retA=solveA(input)

def solveB(input):
    
    count=0
    rng=int(len(input)/3)
    
    for i in range(rng):     
        triangles=[[],[],[]]        
        for j in range(3):
            sides=[int(x) for x in input[(3*i+j)].lstrip().split()]
            for k in range(3):
                triangles[k].append(sides[k])
        for t in triangles:
            t=sorted(t)
            if t[0]+t[1]>t[2]:
                count+=1
    return(count)


retB=solveB(input)