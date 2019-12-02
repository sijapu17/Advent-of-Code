#Advent of Code 2015 Day 8

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-8.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    total=0 #Total difference between memory length and literal length
    for line in input:
        total+=len(line)-len(eval(line))
    return(total)

retA=solveA(input)

def solveB(input):
    total=0
    for line in input:
        total+=2+line.count('\\')+line.count('"')
    return(total)
                     
retB=solveB(input)