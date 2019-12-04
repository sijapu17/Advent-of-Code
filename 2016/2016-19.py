#Advent of Code 2016 Day 19
from collections import deque
import math

input=3001330
#input=5

def solveA(input):
    circle=deque(range(1,input+1))
    while len(circle)>1:
        circle.rotate(-1)
        circle.popleft() #Remove elf from circle
    return(circle.pop())

#retA=solveA(input)


def solveB(input):

    circleL=deque(range(1,math.ceil(input/2)))
    circleR=deque(range(math.ceil(input/2),input+1))
    parity=input%2 #Check whether input is odd or even
    while len(circleL)+len(circleR)>1:
        if parity==0: #If even, move one elf from right half to left
            circleL.append(circleR.popleft())
        #print(str(circleL)+'|'+str(circleR))
        circleR.popleft() #Remove elf from circle
        circleR.append(circleL.popleft())
        #print(str(circleL)+'|'+str(circleR))
        parity=1-parity
    winner=circleR.pop()
    return(winner)


retB=solveB(input)