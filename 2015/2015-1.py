#Advent of Code 2015 Day 1

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2015-1.txt')
contents = f.read()
#input = contents.splitlines()

def solveA(input):
    floor=0
    for i in input:
        if i=='(':
            floor+=1
        else:
            floor-=1
    return(floor)
        
def solveB(input):
    floor=0
    pos=1
    for i in input:
        if i=='(':
            floor+=1
        else:
            floor-=1
        if floor<0:
            return(pos)
        pos+=1

retA=solveA(contents)
retB=solveB(contents)