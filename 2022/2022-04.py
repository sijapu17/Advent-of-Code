#Advent of Code 2022 Day 4

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-04.txt')
contents = f.read()
input = contents.splitlines()

def parse(inp): #Parse input file into pairs of intervals
    p=re.compile('^(\d+)-(\d+),(\d+)-(\d+)$') #regex for lines   
    lines=[] 
    for line in inp:
        m=re.match(p,line)
        x1, x2, y1, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        l=(x1, x2, y1, y2)
        lines.append(l)
    return(lines)

def count_full_overlaps(inp): #Count number of lines where one interval fully covers the other
    count=0
    for l in inp:
        if (l[0]<=l[2] and l[1]>=l[3]) or (l[0]>=l[2] and l[1]<=l[3]):
            count+=1
    return(count)

def count_any_overlaps(inp): #Count number of lines where one interval fully or partially covers the other
    count=0
    for l in inp:
        if l[0]<=l[2]<=l[1] or l[0]<=l[3]<=l[1] or l[2]<=l[1]<=l[3] or l[2]<=l[0]<=l[3]: #Intervals overlap if endpoint of one interval is within the other interval
            count+=1
    return(count)

lines=parse(input)
print(count_full_overlaps(lines))
print(count_any_overlaps(lines))