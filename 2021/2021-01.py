#Advent of Code 2021 Day 1

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-01.txt')
contents = f.read()
input = [int(x) for x in contents.splitlines()]



def solveA(input):
    n=len(input)
    count=0
    for i in range(n-1):
        if input[i+1]>input[i]: #Compare if term is greater than previous
            count+=1
    return(count)

retA=solveA(input)
print(retA)

def solveB(input):
    n=len(input)
    count=0
    for i in range(n-3):
        if sum(input[i+1:i+4])>sum(input[i:i+3]): #Compare if rolling average is greater than previous
            count+=1
    return(count)

retB=solveB(input)
print(retB)