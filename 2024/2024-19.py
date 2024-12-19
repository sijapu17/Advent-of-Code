#Advent of Code 2024 Day 19

from functools import cache

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-19.txt')
contents = f.read()
input = contents.splitlines()

towels=input[0].split(', ')
patterns=tuple(input[2:])

@cache
def count_ways(pattern):
    if pattern=='':
        return(1)    
    ways=0
    for t in towels:
        if pattern.find(t)==0:
            ways+=count_ways(pattern[len(t):])
    return(ways)

print(sum([count_ways(p)>0 for p in patterns]))
print(sum([count_ways(p) for p in patterns]))