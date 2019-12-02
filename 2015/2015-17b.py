#Advent of Code 2015 Day 17

from collections import defaultdict
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-17.txt')
contents = f.read()
input = contents.splitlines()

def impConts(Input): #Import list of containers
    out={}
    for i in range(len(Input)):
        out[i]=int(input[i])
    return(out)

def capacity(conts,ContDict): #Capacity of a list of containers
    sum=0
    for c in conts:
        sum+=ContDict[c]
    return(sum)

def eMax(List):
    if len(List)==0:
        return(-1)
    else:
        return(max(List))

contDict=impConts(input) #Dictionary of containers with capacities

def solveB(ContDict,totCapa):
    sols=defaultdict(int) #Number of correct solutions
    toCheck=[[]]
    while len(toCheck)>0:
        member=toCheck.pop()
        for c in ContDict: #Try to add each unused container in turn
            if c > eMax(member):
                candidate=member[:]+[c]
                capa=capacity(candidate,ContDict)
                l=len(candidate)
                if capa==totCapa:
                    sols[l]+=1 #If solution is found, add one to total for that length
                    print(candidate)
                elif capa<totCapa:
                    toCheck.append(candidate) #If there is spare capacity then return to stack to add containers
    return(sols)

retB=solveB(contDict,150)

                