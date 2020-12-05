#Advent of Code 2020 Day 5

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-05.txt')
contents = f.read()
input=contents.splitlines()

def getID(seat): #Convert seat string into numeric ID
    ID=0
    mul=1 #Rightmost letter corresponds to 1s column, double this for each step left
    for s in reversed(seat):
        if s in ('B','R'):
            ID+=mul
        mul*=2
    return(ID)

def highestID(input):
    IDs=set() #Set of seat IDs
    for x in input:
        IDs.add(getID(x))
    return(max(IDs))

def findMissing(input): #Find missing seat with non-missing seats surrounding it
    IDs=set() #Set of seat IDs
    for x in input:
        IDs.add(getID(x))
    n=0
    while True:
        if n not in IDs:
            if n-1 in IDs and n+1 in IDs:
                return(n)
        n+=1
      

print(highestID(input))
print(findMissing(input))