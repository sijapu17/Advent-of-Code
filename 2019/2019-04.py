#Advent of Code 2019 Day 4

start=264360
end=746325

def adjacent(s): #Checks whether a number (in string form) contains two adjacent digits the same
    for d in range(len(s)-1):
        if s[d]==s[d+1]:
            return(True)
    return(False)

def nextNonDec(s): #Given a number (in string form), returns the next number with no decreasing digits (including the input number)
    update=False
    ret=s[0] #Output string
    for d in range(1,len(s)):
        if update:
            ret+=newDigit
        elif s[d]<s[d-1]:
            update=True #Flag that this number needs to be increased
            newDigit=s[d-1] #Set every digit after the decrease point to the digit before the decrease
            ret+=newDigit
        else:
            ret+=s[d]
    return(ret)

def countCandidates(rLo,rHi): #Count number of possible password within range that meet rules
    i=rLo
    count=0
    while i<=rHi:
        s=nextNonDec(str(i)) #Convert to string for checks, skip to next non-decreasing number
        if adjacent(s) and int(s)<=rHi:
            #print(s)
            count+=1
        i=int(s)+1
    return(count)

retA=countCandidates(start,end)

##### Part B #####

def adjacentB(s): #Checks whether a number (in string form) contains an instance of exactly two adjacent digits the same
    padded='X'+s+'X' #Pad end to allow a 3-digit check without going out of range 
    for d in range(1,len(s)):
        if padded[d-1]!=padded[d] and padded[d]==padded[d+1] and padded[d+1]!=padded[d+2]:
            return(True)
    return(False)

def countCandidatesB(rLo,rHi): #Count number of possible password within range that meet rules
    i=rLo
    count=0
    while i<=rHi:
        s=nextNonDec(str(i)) #Convert to string for checks, skip to next non-decreasing number
        if adjacentB(s) and int(s)<=rHi:
            #print(s)
            count+=1
        i=int(s)+1
    return(count)

retB=countCandidatesB(start,end)