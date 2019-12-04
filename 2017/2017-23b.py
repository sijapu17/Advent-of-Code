#Advent of Code 2017 Day 23

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2017-23.txt')
contents = f.read()
input = contents.splitlines()

def isPrime(n): #Checks whether number is prime
    i=2
    while i<=n**0.5:
        if n%i==0:
            return(False)
        i+=1
    return(True)

def solveB(input):
    b=109900
    c=126900
    tot=0
    for n in range(b,c+1,17):
        if not isPrime(n):
            tot+=1
            print(str(n))
    return(tot)

retA=solveB(input)