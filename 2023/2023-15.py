#Advent of Code 2023 Day 15

from collections import defaultdict
import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-15.txt')
contents = f.read()
input = contents.split(',')

def HASH(instring:str): #Encode string according to HASH function
    current=0
    for s in instring:
        current=((current+ord(s))*17)%256
    return(current)

#print(sum([HASH(x) for x in input]))

class Lens():
    def __init__(self,label,focus) -> None:
        self.label=label
        self.focus=focus #Focal length from 1 to 9

    def __str__(self) -> str:
        return(f'[{self.label} {self.focus}]')
    
    def __repr__(self) -> str:
        return(self.__str__())

def set_lenses(input): #Set up lenses according to input instructions
    p1=re.compile('(\w+)\-') #Pattern for - instruction
    p2=re.compile('(\w+)\=(\d+)') #Pattern for = instruction
    for inst in input:
        m1=p1.match(inst)
        m2=p2.match(inst)
        if m1: # - case: remove labeled lens from box
            label=m1.group(1)
            hash=HASH(label) #Box number
            for l in boxes[hash]:
                if l.label==label:
                    boxes[hash].remove(l)
                    break
        elif m2: # = case: add or replace lens
            label=m2.group(1)
            focus=int(m2.group(2))
            hash=HASH(label) #Box number
            replaced=False
            for l in boxes[hash]:
                if l.label==label:
                    l.focus=focus
                    replaced=True
                    break
            if not replaced:
                boxes[hash].append(Lens(label,focus))

def focusing_power(boxes): #Sum up total focusing power of all lenses
    sum=0
    for n,box in boxes.items():
        for i in range(len(box)):
            lens=box[i]
            sum+=(n+1)*(i+1)*lens.focus
    return(sum)

boxes=defaultdict(list) #Boxes from 0 to 255
set_lenses(input)
print(focusing_power(boxes))