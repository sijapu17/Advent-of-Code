#Advent of Code 2020 Day 10

from collections import defaultdict
from itertools import combinations

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-10.txt')
contents = f.read()
input=sorted([int(x) for x in contents.splitlines()])

def find_jump_dist(input): #Find number of 1-volt jumps and 3-volt jumps
    counts=defaultdict(int) # Count jumps of different sizes
    for i in range(len(input)-1):
        counts[input[i+1]-input[i]]+=1   
    counts[input[0]]+=1 #Add jump from socket to lowest adaptor
    counts[3]+=1 #Add jump from highest adaptor to device
    return(counts[1]*counts[3])

print(find_jump_dist(input))

def split_list(input): #Split list into minilists which only increase by 1
    current=[0]
    for i in range(len(input)-1):
        current.append(input[i])
        if input[i+1]-input[i]==3:
            yield(current)
            current=[]
    current.append(input[-1])
    yield(current)

def count_combs(minilist): #Count combinations of adaptors in minilist, ensuring adaptors at both ends are included and no gap is >3
    count=0
    for i in range(min(2,len(minilist)),len(minilist)+1): #Check combinations of all lengths from 2 (just the ends) to the full minilist for validity
        for c in combinations(minilist, i):
            if minilist[0] in c and minilist[-1] in c: #Check ends
                valid=True
                for j in range(len(c)-1):
                    if c[j+1]-c[j]>3:
                        valid=False
                        break
                count+=valid
                #print(str(c)+': '+str(valid))
    return(count)

def solveB(list): #Split list at every jump of 3, and multiply together number of combinations for each minilist
    combs=1
    for mini in split_list(input):
        print(str(mini))
        combs*=count_combs(mini)
    return(combs)

print(solveB(input))
