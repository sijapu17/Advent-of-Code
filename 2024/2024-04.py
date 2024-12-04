#Advent of Code 2024 Day 4

from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-04.txt')
contents = f.read()
input = contents.splitlines()

text=defaultdict(str)

#Set up defaultdict of letter locations
xmax=len(input[0])
ymax=len(input)
for j in range(ymax):
    for i in range(xmax):
        text[complex(i,j)]=input[j][i]

#Part 1
matches=0
#Horizontal matches
for y in range(ymax):
    for x in range(xmax):
        if ''.join([text[complex(x+i,y)] for i in range(4)]) in ('XMAS','SAMX'):
            matches+=1
#Vertical matches
for x in range(xmax):
    for y in range(ymax):
        if ''.join([text[complex(x,y+j)] for j in range(4)]) in ('XMAS','SAMX'):
            matches+=1
#+ve Diagonal matches
for x in range(xmax):
    for y in range(ymax):
        if ''.join([text[complex(x+j,y+j)] for j in range(4)]) in ('XMAS','SAMX'):
            matches+=1
#-ve Diagonal matches
for x in range(xmax):
    for y in range(3,ymax+4):
        if ''.join([text[complex(x+j,y-j)] for j in range(4)]) in ('XMAS','SAMX'):
            matches+=1
print(matches)

#Part 2
matches=0

#X matches
for x in range(xmax):
    for y in range(ymax):
        if text[complex(x,y)]=='A' and {text[complex(x-1,y-1)],text[complex(x+1,y+1)]}=={'M','S'} and {text[complex(x-1,y+1)],text[complex(x+1,y-1)]}=={'M','S'}:
            matches+=1

print(matches)