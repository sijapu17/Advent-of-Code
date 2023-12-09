#Advent of Code 2023 Day 9

import re
from itertools import pairwise

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-09.txt')
contents = f.read()
input = contents.splitlines()

rows=[]

for r in input:
    rows.append([int(x) for x in re.findall(r"-?\d+",r)])

rev_rows=[x[::-1] for x in rows]

def is_zeroes(r):
    return(min(r)==0 and max(r)==0)

def find_next(row): #Find next number in polynomial sequence
    current=row
    diffs=[current]
    while not is_zeroes(current): #Calculate differences
        new=[y - x for x, y in pairwise(current)]
        current=new
        diffs.append(current)
    to_add=0
    for i in range(len(diffs)-2,-1,-1):
        to_add+=diffs[i][-1]
    return(to_add)

def sum_values(rows): #Sum next number of each sequence
    sum=0
    for r in rows:
        sum+=find_next(r)
    return(sum)


print(sum_values(rows))
print(sum_values(rev_rows))