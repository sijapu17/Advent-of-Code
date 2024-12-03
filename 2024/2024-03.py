#Advent of Code 2024 Day 3

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-03.txt')
input = f.read()

#Part 1
muls=re.findall(r'mul\((\d{1,3}),(\d{1,3})\)',input)
print(sum([int(a)*int(b) for (a,b) in muls]))

#Part 2
mul_do=re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\)|don't\(\))",input)

total=0
enabled=True
for match in mul_do:
    if match[2]=='do()': #Enable future mul()
        enabled=True
    elif match[2]=="don't()": #Disable future mul()
        enabled=False
    else:
        total+=int(match[0])*int(match[1])*enabled

print(total)