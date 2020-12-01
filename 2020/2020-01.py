#Advent of Code 2020 Day 1

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-01.txt')
contents = f.read()
input = [int(x) for x in contents.splitlines()]



def solveA(input):
    #Find 2 elements that sum to 2020
    n=len(input)
    i=0
    while i<n:
        j=i+1 #For each new i, start j at i+1 and step upwards
        while j<n:
            if input[i]+input[j]==2020:
                return(input[i]*input[j])
            j+=1
        i+=1

retA=solveA(input)
print(retA)

def solveB(input):
    #Find 3 elements that sum to 2020
    n=len(input)
    i=0
    while i<n:
        j=i+1 #For each new i, start j at i+1 and step upwards
        while j<n:
            if input[i]+input[j]>=2020: #If i,j pair sums to >2020, skip it
                j+=1
                continue
            k=j+1 #For each new j, start k at j+1 and step upwards
            while k<n:
                if input[i]+input[j]+input[k]==2020:
                    return(input[i]*input[j]*input[k])
                k+=1
            j+=1
        i+=1

retB=solveB(input)
print(retB)