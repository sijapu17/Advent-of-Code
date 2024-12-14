#Advent of Code 2024 Day 14

import re
from collections import Counter
from math import prod

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-14.txt')
contents = f.read()
input = contents.splitlines()
in_re=[[int(x) for x in re.findall(r'(-?\d+)',y)] for y in input]
#maxX, maxY = 11, 7
maxX, maxY = 101, 103

class Robot:
    def __init__(self,input):
        self.p_x, self.p_y, self.v_x, self.v_y=input

    def find_pos(self,t): #Calculate position at time t
        x=(self.p_x+self.v_x*t)%maxX
        y=(self.p_y+self.v_y*t)%maxY
        return((x,y))
    
    def find_quadrant(self,t): #Calculate quadrant at time t:
        p_x, p_y=self.find_pos(t)
        if p_x<maxX//2 and p_y<maxY//2:
            return(1)
        elif p_x>maxX//2 and p_y<maxY//2:
            return(2)
        elif p_x<maxX//2 and p_y>maxY//2:
            return(3)
        elif p_x>maxX//2 and p_y>maxY//2:
            return(4)
        else:
            return(0)

def print_bots(coords):
    ret=''
    for j in range(maxY):
        for i in range(maxX):
            if (i,j) in coords:
                ret+='#'
            else:
                ret+='.'
        ret+='\n'
    return(ret)

robots=[Robot(x) for x in in_re]
counts=Counter([r.find_quadrant(100) for r in robots])
del counts[0] #Remove quadrantless robots
print(prod(counts.values()))

max_closeness=0
for t in range(10000):
    bots={r.find_pos(t) for r in robots}
    #Calculate closeness score
    closeness=0
    for p in bots:
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if (p[0]+i, p[1]+j) in bots:
                    closeness+=1
    if closeness>max_closeness: #Hidden picture will occur when many bots are close to each other
        print(f't={t}, closeness={closeness}:')
        print(print_bots(bots))
        max_closeness=closeness

