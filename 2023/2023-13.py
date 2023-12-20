#Advent of Code 2023 Day 13

from itertools import groupby
from math import log2

def power2(n): #Check if n is a power of 2
    return(log2(n).is_integer())

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-13.txt')
contents = f.read()
input = contents.splitlines()

#Split input into blocks
blocks = [list(sub) for x, sub in groupby(input, key = bool) if x]

#Convert each row into an integer, reading as a binary number where #=1, .=0
rows=[]
for b in blocks:
    row=[]
    for r in b:        
        row.append(sum([2**i if r[i]=='#' else 0 for i in range(len(r))]))
    rows.append(row)

#Convert each col into an integer, reading as a binary number where #=1, .=0
cols=[]
for b in blocks:
    col=[]
    for i in range(len(b[0])):        
        col.append(sum([2**j if b[j][i]=='#' else 0 for j in range(len(b))]))
    cols.append(col)

#Find index of reflective midpoint (if any)
def reflectpoint(line): 
    for n in range(len(line)-1):
        l1=list(reversed(line[:n+1]))
        l2=line[n+1:]
        minlen=min(len(l1),len(l2))
        if l1[:minlen]==l2[:minlen]:
            return(n+1) #Account for 1-indexing in problem
    return(0)

#Compare bits of two numbers to see if they're equal, differ by 1 bit or differ by more bits
def compare_bits(n1,n2): 
    if n1==n2:
        return(0)
    diff=n1^n2
    if power2(diff):
        return(1)
    else:
        return(2)

#Find index of reflective midpoint (if any) where exactly one bit is flipped
def reflectpointsmudge(line): 
    for n in range(len(line)-1):
        l1=list(reversed(line[:n+1]))
        l2=line[n+1:]
        minlen=min(len(l1),len(l2))
        s=sum([compare_bits(a,b) for a,b in zip(l1[:minlen],l2[:minlen])])
        if s==1: #Return if exactly 1 bit differs across line
            return(n+1) #Account for 1-indexing in problem
    return(0)

#Calculate score for each row/column where reflection is found
def rowcolscore(part): 
    sum=0
    for n in range(len(blocks)):
        if part==1:
            c=reflectpoint(cols[n])
            r=reflectpoint(rows[n])
        elif part==2:
            c=reflectpointsmudge(cols[n])
            r=reflectpointsmudge(rows[n])
           
        print(f'{n}: c={c},r={r}')
        sum+=c
        sum+=r*100
    return(sum)

print(rowcolscore(1))
print(rowcolscore(2))