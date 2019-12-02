#Advent of Code 2019 Day 1

import math

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-01.txt')
contents = f.read()
input = contents.splitlines()

def calcFuel(m): #Returns mass of fuel required to launch mass m
    return(math.floor(m/3-2))

def calcFuelB(m): #Returns mass of fuel required to launch mass m, including fuel required to launch fuel
    ret=0
    rem=calcFuel(m)
    while rem>0:
        ret+=rem #Add remaining mass to total
        rem=calcFuel(rem) #Calculate how much fuel required to launch that mass
    return(ret)

def solveA(input):
    masses=[int(x) for x in input]
    ret=0
    for m in masses:
        ret+=calcFuel(m)
    return(ret)

retA=solveA(input)

def solveB(input):
    masses=[int(x) for x in input]
    ret=0
    for m in masses:
        ret+=calcFuelB(m)
    return(ret)

retB=solveB(input)
