#Advent of Code 2020 Day 2

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-02.txt')
contents = f.read()
#regex to parse input lines
p1=re.compile('^(\d+)\-(\d+) (\w): (.+)$')
input =[]
for x in contents.splitlines():
    m1=p1.match(x)
    input.append([int(m1.group(1)),int(m1.group(2)),m1.group(3),m1.group(4)])

def solveA(input):
    valid=0
    for line in input:
        #Count occurrences of letter in password
        reps=line[3].count(line[2])
        #If number of reps is within limits, increment count
        if line[0]<=reps<=line[1]:
            valid+=1
    print(valid)

solveA(input)

def solveB(input):
    valid=0
    for line in input:
        #Check whether the character is in one of the specified positions (but not both)
        if line[3][line[0]-1]==line[2] or line[3][line[1]-1]==line[2]:
            if not(line[3][line[0]-1]==line[2] and line[3][line[1]-1]==line[2]):
                valid+=1
    print(valid)

solveB(input)   
