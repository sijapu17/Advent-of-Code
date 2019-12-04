#Advent of Code 2018 Day 1


f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-1.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    sum=0
    for i in input:
        sum+=int(i)
    return(sum)

#retA=solveA(input)

def solveB(input):
    sum=0
    n=0
    seen=set()
    while True:
        for i in input:
            sum+=int(i)
            if sum in seen:
                print(str(n)+' loops')
                return(sum)
            seen.add(sum)
        n+=1

retB=solveB(input)