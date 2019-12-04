#Advent of Code 2018 Day 9
from collections import defaultdict
from collections import deque

nElves=412
nMarbles=71646 #include marble 0

def solveAlist(nElves,nMarbles):
    circle=[0] #Start with current marble
    curPos=0 #Position of current marble
    curElf=0 #Number of current elf
    n=1 #Number of marble to be placed
    scores=defaultdict(int)
    while n<=nMarbles:
        if n%100000==1:
            print('Step '+str(n))
        l=len(circle)
        if n%23==0:
            scores[curElf]+=n
            curPos=(curPos-7)%l
            scores[curElf]+=circle[curPos]
            del circle[curPos]
        else:
            curPos=(curPos+2)%l
            circle.insert(curPos,n)
        n+=1
        curElf=(curElf+1)%nElves
    #print(circle)
    #return(scores)
    return(max(scores.values()))

#nMarbles=6111
#nElves=21

def solveA(nElves,nMarbles):
    circle=deque([0]) #Start with current marble
    curElf=0 #Number of current elf
    n=1 #Number of marble to be placed
    scores=defaultdict(int)
    while n<=nMarbles:
        if n%1000000==1:
            print('Step '+str(n))
        if n%23==0:
            scores[curElf]+=n
            circle.rotate(7)
            scores[curElf]+=circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(n)
        n+=1
        curElf=(curElf+1)%nElves
        #print(circle)
    #return(scores)
    return(max(scores.values()))

#nElves=10
#nMarbles=25

retA=solveA(nElves,nMarbles)

nElves=412
nMarbles=7164600 #include marble 0
        
retB=solveA(nElves,nMarbles)


