#Advent of Code 2024 Day 25

from itertools import product

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-25.txt')
contents = f.read()
input = contents.splitlines()

keys=[]
locks=[]
y=0
while y<len(input):
    vals=[-1]*5 #Start count at -1 to offset solid row
    for j in range(7):
        for i in range(5):
            vals[i]+=input[y+j][i]=='#'
    if input[y][0]=='#':
        locks.append(vals)
    else:
        keys.append(vals)
    y+=8

def lock_key_fits(lock,key):
    return(max([lock[i]+key[i] for i in range(5)])<=5)

print(sum([lock_key_fits(l,k) for l,k in product(locks,keys)]))