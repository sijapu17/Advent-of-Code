#Advent of Code 2022 Day 5

import re
from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-05.txt')
contents = f.read()
input = contents.splitlines()

def parse(): #Parse input text file into stacks of crates and instructions
    global crates
    global moves
    crates=defaultdict(list) #Dict of which crates are on each numbered stack
    moves=[] #List of moves to be performed
    p=re.compile('^move (\d+) from (\d+) to (\d+)$') #regex for lines
    for x in input:
        #Lines with crates
        if len(x)>0 and x[0] in '[ ' and x[1]!='1': 
            cr_in=x[1::4]
            for i in range(len(cr_in)):
                if cr_in[i]!=' ':
                    crates[i+1].insert(0,cr_in[i])
        #Lines with move instructions
        if re.search(p,x):
            m=re.search(p,x)
            moves.append((int(m.group(1)),int(m.group(2)),int(m.group(3))))



def move_crates(part): #Move crates following each instruction in order
    for m in moves:
        num, frm, to = m
        moving=[] #Stack of crates that are being moved
        for i in range(num):
            moving.append(crates[frm].pop())
        if part==1:
            moving.reverse()
        for i in range(num):
            crates[to].append(moving.pop())        

def read_tops(): #Return the letter of the top crate in each stack
    out=''
    for i in range(len(crates)):
        out+=crates[i+1][-1]
    return(out)

parse()   
move_crates(part=1)     
print(read_tops())
parse()   
move_crates(part=2)     
print(read_tops())