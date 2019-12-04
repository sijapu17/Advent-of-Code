#Advent of Code 2017 Day 9

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-9.txt')
input = f.read()

def excRemove(input):
    in1=input
    out=''
    i=0
    while (i<len(in1)):
        if in1[i]=='!':
            i+=2 #Skip '!' and character after it
        else:
            out+=in1[i]
            i+=1
    return(out)

def GarbageRemove(input):
    in1=input
    out=''
    i=0
    ingarb=0
    while (i<len(in1)):
        if (in1[i]=='!' and ingarb==1):
            i+=2 #Skip '!' and character after it within garbage
        elif in1[i]=='<':
            ingarb=1
            i+=1
        elif in1[i]=='>':
            ingarb=0
            i+=1
        else:
            if ingarb==0:
                out+=in1[i]
            i+=1
    return(out)

#stage1=GarbageRemove(input)

def solveA(input):
    in1=input
    i=0
    nest=0
    score=0
    while (i<len(in1)):
        if in1[i]=='{':
            nest+=1
            score+=nest
        elif in1[i]=='}':
            nest-=1
        i+=1
    print('Final nest='+str(nest))
    return(score)

#retA=solveA(stage1)
    
def solveB(input):
    in1=input
    out=''
    i=0
    ingarb=0
    total=0
    while (i<len(in1)):
        if (in1[i]=='!' and ingarb==1):
            i+=2 #Skip '!' and character after it within garbage
        elif (in1[i]=='<' and ingarb==0):
            ingarb=1
            i+=1
        elif in1[i]=='>':
            ingarb=0
            i+=1
        else:
            if ingarb==1:
                total+=1 #Count characters inside garbage which have not been cancelled by !
            i+=1
    return(total)

retB=solveB(input)