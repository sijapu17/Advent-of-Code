#Advent of Code 2025 Day 7
from functools import cache

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-07.txt')
contents = f.read()
input = contents.splitlines()

splitters=set()
x_max=len(input[0])
y_max=len(input)

#Import map
for j in range(y_max):
    for i in range(x_max):
        if input[j][i]=='^':
            splitters.add(complex(i,j))
        elif input[j][i]=='S':
            start_pos=complex(i,j)

#Count number of splitters used
splitters_used=set()

#Recursive function to count number of timelines from given position
@cache
def timelines_from_pos(pos):
    current=pos
    while True:
        #Beam hits any splitter: split
        if current in splitters:
            splitters_used.add(current)
            return(timelines_from_pos(current+complex(-1,0))+timelines_from_pos(current+complex(1,0)))
        #Beam falls below map: one timeline
        elif current.imag>y_max:
            return(1)
        else: #Else drop down one space
            current+=complex(0,1)

print(timelines_from_pos(start_pos)) #Part 2
print(len(splitters_used)) #Part 1