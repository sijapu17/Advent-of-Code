#Advent of Code 2018 Day 19

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-19.txt')
contents = f.read()
input=contents.splitlines()

import re

def addr(reg,a,b,c):
    reg[c]=reg[a]+reg[b]
def addi(reg,a,b,c):
    reg[c]=reg[a]+b
def mulr(reg,a,b,c):
    reg[c]=reg[a]*reg[b]
def muli(reg,a,b,c):
    reg[c]=reg[a]*b
def banr(reg,a,b,c):
    reg[c]=reg[a]&reg[b]   
def bani(reg,a,b,c):
    reg[c]=reg[a]&b
def borr(reg,a,b,c):
    reg[c]=reg[a]|reg[b]    
def bori(reg,a,b,c):
    reg[c]=reg[a]|b
def setr(reg,a,b,c):
    reg[c]=reg[a]    
def seti(reg,a,b,c):
    reg[c]=a
def gtir(reg,a,b,c):
    if a>reg[b]:
        reg[c]=1
    else:
        reg[c]=0
def gtri(reg,a,b,c):
    if reg[a]>b:
        reg[c]=1
    else:
        reg[c]=0
def gtrr(reg,a,b,c):
    if reg[a]>reg[b]:
        reg[c]=1
    else:
        reg[c]=0
def eqir(reg,a,b,c):
    if a==reg[b]:
        reg[c]=1
    else:
        reg[c]=0
def eqri(reg,a,b,c):
    if reg[a]==b:
        reg[c]=1
    else:
        reg[c]=0
def eqrr(reg,a,b,c):
    if reg[a]==reg[b]:
        reg[c]=1
    else:
        reg[c]=0

def parse(input):
    instrs={}
    instrs['pointer']=int(input.pop(0).split()[1])
    p1=re.compile('(\w+) (\d+) (\d+) (\d+)')
    i=0
    for x in input:
        m1=p1.match(x)
        inst=m1.group(1)+'(reg,'+m1.group(2)+','+m1.group(3)+','+m1.group(4)+')'
        instrs[i]=inst
        i+=1
    return(instrs)

def solveA(instrs):
    reg={}
    for r in range(6):
        reg[r]=0
    pointer=instrs['pointer']
    n=0
    while True:
        if reg[pointer] in instrs:
            inst=instrs[reg[pointer]]
            print(reg)
            print(str(reg[pointer])+': '+inst)
            eval(inst)
            #if n%10000==1:
            #print(str(n))
            reg[pointer]+=1 #Move onto next instruction
            n+=1
        else:
            return(reg)
        

instrs=parse(input)
#retA=solveA(instrs)

def solveB(instrs):
    reg={}
    reg[0]=1
    for r in range(1,6):
        reg[r]=0
    pointer=instrs['pointer']
    n=0
    while reg[pointer]!=1:
        if reg[pointer] in instrs:
            inst=instrs[reg[pointer]]
            print(reg)
            print(str(reg[pointer])+': '+inst)
            eval(inst)
            #if n%10000==1:
            #print(str(n))
            reg[pointer]+=1 #Move onto next instruction
            n+=1
        else:
            return(reg)
    return(reg)
       
#Part 2
#reg[0]=1
#initB=solveB(instrs)


def sumDivisors(input):
    sum=0
    for i in range(1,int(round((input**0.5)+1))):
        j=input/i
        if round(j)==j:
            sum+=int(i+j)
    return(sum)

#retA=sumDivisors(948)
retB=sumDivisors(10551348)