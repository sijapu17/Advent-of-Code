#Advent of Code 2020 Day 14

from collections import defaultdict
import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-14.txt')
contents = f.read()
input=contents.splitlines()

def applyMasks(input):
    
    mem=defaultdict(int) #All memory positions set to 0 by default
    p=re.compile('^mem\[(\d+)\] = (\d+)$')
    for l in input:
        if l.split()[0]=='mask': #Set up new mask
            mask0=int(l.split()[2].replace('X','1'),base=2) #Mask to set bytes of mem to 0
            mask1=int(l.split()[2].replace('X','0'),base=2) #Mask to set bytes of mem to 1
        
        else: #Otherwise apply masks to specified memory position
            m=p.match(l) #Use regex to extract numbers from instruction
            pos=int(m.group(1))
            val=int(m.group(2))
            val&=mask0
            val|=mask1
            mem[pos]=val

    #Result is sum of non-zero values in mem
    return(sum(mem.values()))

print(applyMasks(input))

def applyMasksFloating(input):
    
    mem=defaultdict(int) #All memory positions set to 0 by default
    p=re.compile('^mem\[(\d+)\] = (\d+)$')
    for l in input:
        if l.split()[0]=='mask': #Set up new masks
            masks=[]
            queue=[]
            queue.append(l.split()[2].replace('0','x')) #0 in new mask means leave byte unchanged
            while len(queue)>0:
                current=queue.pop()
                pos=current.find('X')
                if pos==-1: #If no X is found then no more splits needed
                    masks.append(current)
                else: #Split the first X found into a 0 version and a 1 version
                    queue.append(current[:pos]+'0'+current[pos+1:])
                    queue.append(current[:pos]+'1'+current[pos+1:])

            masks0=[int(y.replace('x','1'),base=2) for y in masks] #Masks to set bytes of mem to 0
            masks1=[int(y.replace('x','0'),base=2) for y in masks] #Masks to set bytes of mem to 1
        
        else: #Otherwise apply masks to specified memory position
            m=p.match(l) #Use regex to extract numbers from instruction
            pos=int(m.group(1))
            val=int(m.group(2))
            for i in range(len(masks0)):
                pos1=pos #Create copy of pos so only one mask pair is applied at a time
                pos1&=masks0[i]
                pos1|=masks1[i]
                mem[pos1]=val

    #Result is sum of non-zero values in mem
    return(sum(mem.values()))

print(applyMasksFloating(input))