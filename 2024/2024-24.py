#Advent of Code 2024 Day 24

from collections import deque
import re
from itertools import combinations

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-24.txt')
contents = f.read()
input = contents.splitlines()

class Gate():
    def __init__(self,in_A,op,in_B,out,swaps):
        self.in_A=min(in_A,in_B)
        self.in_B=max(in_A,in_B)
        self.op=op
        if out in swaps.keys():
            self.out=swaps[out]
        else:
            self.out=out

    def __str__(self):
        return(f'{self.in_A} {self.op:3} {self.in_B} > {self.out}')
    
    def __repr__(self):
        return(self.__str__())


def process_system(x=None,y=None,swaps={}):
    #Import gates and wires
    wires={}
    gates=deque()
          
    for i in input:
        if i.find(':')>0: #Wire
            n, val=i.split(': ')
            if x is None:
                wires[n]=int(val)
            else: #Initialise to 0 if user values have been supplied
                wires[n]=0
        elif i.find('->')>0: #Gate
            gates.append(Gate(*re.findall(r'(\w+)',i),swaps))

    if x is not None:
        x_bin=str(bin(x))[2:][::-1]
        for m in range(len(x_bin)):
            wires[f'x{m:02}']=int(x_bin[m])
    if y is not None:
        y_bin=str(bin(y))[2:][::-1]
        for n in range(len(y_bin)):
            wires[f'y{n:02}']=int(y_bin[n]) 
    #print(wires)
    #print(sorted(gates,key=lambda g:g.out))

    #Sort gates into expected order
    sorted_gates=[]
    n=0 #Current bit
    i=0
    next_n_up=2
    while len(gates)>0 and n<=46:
        i+=1
        if i>500:
            break
        mod=len(sorted_gates)%5
        if len(sorted_gates)==next_n_up: #First bit has 2 gates, higher bits have 5 gates
            n+=1
            next_n_up+=5
        g=gates.pop()
        m=False
        if len(sorted_gates)<2: #First find initial x00, y00 gates
            if g.in_A=='x00':
                m=True
                if g.op=='AND':
                    c_in=g.out
        else:
            match mod:
                case 2: #A: Xnn XOR Ynn
                    m=g.in_A==f'x{n:02}' and  g.op=='XOR' and g.in_B==f'y{n:02}'
                    if m:
                        gate_a=g.out
                case 3: #B: Xnn AND Ynn
                    m=g.in_A==f'x{n:02}' and  g.op=='AND' and g.in_B==f'y{n:02}'
                    if m:
                        gate_b=g.out
                case 4: #C: A XOR C_IN (out=Znn)
                    m=(gate_a in (g.in_A, g.in_B) and g.op=='XOR') and g.out==f'z{n:02}'
                case 0: #D: A AND C_IN 
                    m= gate_a in (g.in_A, g.in_B) and g.op=='AND'
                    if m:
                        gate_d=g.out
                case 1: #E: B  OR D (out=C_OUT)
                    m= (gate_b in (g.in_A, g.in_B) or gate_d in (g.in_A, g.in_B)) and g.op=='OR'
        if m:
            sorted_gates.append(g)
            #print(f'{n}/{mod}: {g}')
            i=0
        else:
            gates.appendleft(g)

    #Process gates
    for g in sorted_gates:
            #print(g)
            if g=='BLANK':
                break
            match g.op:
                case 'AND':
                    wires[g.out]=wires[g.in_A]&wires[g.in_B]
                case 'OR':
                    wires[g.out]=wires[g.in_A]|wires[g.in_B]
                case 'XOR':
                    wires[g.out]=wires[g.in_A]^wires[g.in_B]

    z_keys=reversed(sorted({k:v for k,v in wires.items() if k[0]=='z'}))
    z_bin=''.join(str(wires[x]) for x in z_keys)
    #print(z_bin)
    return((int(z_bin,2)))

print(process_system()) #Part 1

swaps={'gjc':'qjj','qjj':'gjc','gvm':'z26','z26':'gvm','wmp':'z17','z17':'wmp','qsb':'z39','z39':'qsb'}
print(process_system(swaps=swaps)) #Part 2
print(','.join(sorted(swaps.keys())))
def test_value(nx,ny):
    res=process_system(nx,ny)
    if res!=nx+ny:
        print(f'{nx}+{ny}={res} is incorrect, should be {nx+ny}')
        return(False)
    else:
        print(f'{nx}+{ny}={res} is correct')
        return(True)

#test_value(1,0)