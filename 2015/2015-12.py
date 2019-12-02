#Advent of Code 2015 Day 12

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-12.txt')
input = f.read()

num='-0123456789'

def solveA(input):
    sum=0
    current=''
    for c in input:
        if c in num:
            current+=c
        elif len(current)>0:
            sum+=int(current)
            current=''
    return(sum)

retA=solveA(input)