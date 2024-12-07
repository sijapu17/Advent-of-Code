#Advent of Code 2024 Day 7

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-07.txt')
contents = f.read()
input = contents.splitlines()

class Equation():
    def __init__(self,inp) -> None:
        m=[int(x) for x in re.findall(r'(\d+)',inp)]
        self.lhs=m[0]
        self.rhs=m[1:]

    def evaluate(self): #Evaluate whether equation can be balanced by adding and multiplying
        current=set([self.rhs[0]])
        for n in self.rhs[1:]:
            new=[]
            for c in current:
                new.append(c+n)
                new.append(c*n)
            current=set([x for x in new if x<=self.lhs])

        return(self.lhs if self.lhs in current else 0)

    def evaluate2(self): #Evaluate whether equation can be balanced by adding, multiplying and concatenating
        current=set([self.rhs[0]])
        for n in self.rhs[1:]:
            new=[]
            for c in current:
                new.append(c+n)
                new.append(c*n)
                new.append(int(str(c)+str(n)))
            current=set([x for x in new if x<=self.lhs])

        return(self.lhs if self.lhs in current else 0)
    
equations=[]
for i in input:
    equations.append(Equation(i))

#Part 1
print(sum([x.evaluate() for x in equations]))
#Part 2
print(sum([x.evaluate2() for x in equations]))