#Advent of Code 2020 Day 3

from functools import reduce

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-03.txt')
contents = f.read()
input=contents.splitlines()


class Forest(): #Forest of trees and empty spaces

    def __init__(self,input): #Convert input into asteroid list
        self.w=len(input[0])
        self.h=len(input)
        self.map=set() #Set of tree locations
        for c in range(self.h):
            for r in range(self.w):
                if input[c][r]=='#':
                    self.map.add(complex(r,c))

    def __str__(self): #Display map of trees
        ret=''
        for c in range(self.h):
            for r in range(self.w):
                if complex(r,c) in self.map:
                    ret+='#'
                else:
                    ret+='.'
            ret+='\n'
        return(ret)

    def traverse(self,r,d): #Count trees when traversing in steps or r right and d down
        nSteps=self.h//d #Number of steps required to reach or pass the bottom of the map
        nTrees=0 #Count number of trees hit
        pos=complex(0,0) #Current position
        for i in range(nSteps):
            pos=complex((pos.real+r)%self.w,pos.imag+d) #If step goes off right edge of map, loop back through the left edge
            if pos in self.map:
                nTrees+=1
        return(nTrees)



forest=Forest(input)
print(forest)
retA=forest.traverse(r=3,d=1)
print(retA)

#Multiply together results for 5 different trajectories
runs=[forest.traverse(r=1,d=1),forest.traverse(r=3,d=1),forest.traverse(r=5,d=1),forest.traverse(r=7,d=1),forest.traverse(r=1,d=2)]
retB=reduce((lambda x, y: x * y), runs)

print(retB)