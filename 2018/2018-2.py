#Advent of Code 2018 Day 2


f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-2.txt')
contents = f.read()
input = contents.splitlines()

def nInString(text,n): #Check whether a substring of exactly n identical chars exists in a string
    prev=text[0]
    count=1
    for i in range(1,len(text)):
        if text[i]==prev:
            count+=1
        else:
            if count==n:
                return(True)
            count=1
            prev=text[i]
    return(count==n)

t=nInString('aaaab',3)

def solveA(input):
    c2=0
    c3=0
    for b in input:
        s=sorted(b)
        if nInString(s,2):
            c2+=1
        if nInString(s,3):
            c3+=1
    return(c2*c3)

#retA=solveA(input)

def checkDiffs(b1,b2): #Check whether two box IDs have exactly one difference
    diffs=0
    for i in range(len(b1)):
        if b1[i]!=b2[i]:
            diffs+=1
            if diffs>1:
                return(False)
    return(diffs==1)

def solveB(input):
    for b1 in input:
        for b2 in input:
            if checkDiffs(b1,b2):
                ret=''
                for c in range(len(b1)):
                    if b1[c]==b2[c]:
                        ret+=b1[c]
                return(ret)
            
retB=solveB(input)