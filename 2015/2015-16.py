#Advent of Code 2015 Day 16

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-16.txt')
f1 = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-16list.txt')
contents = f.read()
contents1 = f1.read()
input = contents.splitlines()
input1=contents1.splitlines()

def impSues(input):
    sues={}
    for sue in input:
        s=sue.split(': ',1)
        sues[s[0]]={}
        for fact in s[1].split(', '):
            sues[s[0]][fact.split(': ')[0]]=int(fact.split(': ')[1])
    return(sues)

sues=impSues(input)

def impMess(input1):
    mess={}
    for line in input1:
        l1=line.split(': ')
        mess[l1[0]]=int(l1[1])
    return(mess)

message=impMess(input1)

def solveA(sues,message):
    for sue in sues:
        possible=True
        for m in message:
            if m in sues[sue]:
                if message[m]!=sues[sue][m]:
                    possible=False
                    break
        if possible:
            return(sue)
        
retA=solveA(sues,message)