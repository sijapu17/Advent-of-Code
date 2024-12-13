#Advent of Code 2024 Day 13

import re
import sympy

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-13.txt')
contents = f.read()
input = ','.join(contents.splitlines())

in_re=re.findall(r'Button A: X\+(\d+), Y\+(\d+),Button B: X\+(\d+), Y\+(\d+),Prize: X=(\d+), Y=(\d+)',input)

class Machine():
    def __init__(self,input):
        self.a_x, self.a_y, self.b_x, self.b_y, self.p_x, self.p_y=(int(x) for x in input)

    def calculate_tokens(self,offset=0):
        a, b=sympy.symbols('a b')
        eq_x = sympy.Eq(self.a_x*a+self.b_x*b,self.p_x+offset)
        eq_y = sympy.Eq(self.a_y*a+self.b_y*b,self.p_y+offset)      
        #Solve for unknowns
        sols=sympy.solve([eq_x,eq_y],(a,b))
        #print(sols)
        if int(sols[a])==sols[a] and int(sols[b])==sols[b]:
            return(3*sols[a]+sols[b]) #Button A costs 3 tokens, Button B costs 1
        return(0)

machines=[Machine(x) for x in in_re]
print(sum([m.calculate_tokens() for m in machines])) #Part 1
print(sum([m.calculate_tokens(10000000000000) for m in machines])) #Part 2