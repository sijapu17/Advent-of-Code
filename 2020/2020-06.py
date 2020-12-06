#Advent of Code 2020 Day 6

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-06.txt')
contents = f.read()
input=contents.splitlines()

def solveA(input): #Sum of unique answers in each group
    count=0
    current=set()
    for x in input:
        if len(x)==0: #At empty line, add current person to records and start new person
            count+=len(current)
            current=set()
        else:
            current |= set([c for c in x]) #Split line into list of chars, convert to set and union with current set
    count+=len(current) #Count final group
    return(count)

print(solveA(input))

def solveB(input): #Sum of common answers in each group
    count=0
    current=set()
    new=True
    for x in input:
        if len(x)==0: #At empty line, add current person to records and start new person
            count+=len(current)            
            current=set()
            new=True #Indicator for new group
        else:
            if new:
                current=set([c for c in x])
                new=False
            else:
                current &= set([c for c in x]) #Split line into list of chars, convert to set and intersection with current set
    count+=len(current) #Count final group
    return(count)

print(solveB(input))