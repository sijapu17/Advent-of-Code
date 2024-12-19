#Advent of Code 2024 Day 17

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-17.txt')
contents = f.read()
input = contents.splitlines()

class Computer():
    def __init__(self,input,n=None):
        if n is None:
            self.A=int(input[0].split()[-1])
        else:
            self.A=n
        self.B=int(input[1].split()[-1])
        self.C=int(input[2].split()[-1])
        self.program=[int(x) for x in re.findall(r'(\d+)',input[-1])]
        self.pointer=0
        self.prog_out=[]

        self.instructions={0:self.adv,1:self.bxl,2:self.bst,3:self.jnz,4:self.bxc,5:self.out,6:self.bdv,7:self.cdv}

    def combo(self,op): #Return value of combo operand
        match op:
            case 0|1|2|3:
                return(op)
            case 4:
                return(self.A)
            case 5:
                return(self.B)
            case 6:
                return(self.C)
            case _:
                print(f'Bad combo operator {op}')
                return()

    def adv(self,op): #Divide A, store in A
        self.A=self.A//2**self.combo(op)
        self.pointer+=2
    
    def bxl(self,op): #Bitwise XOR B
        self.B=self.B^op
        self.pointer+=2
    
    def bst(self,op): #Modulo 8
        self.B=self.combo(op)%8
        self.pointer+=2

    def jnz(self,op): #Jump if non-zero
        if self.A!=0:
            self.pointer=op
        else:
            self.pointer+=2
    
    def bxc(self,op): #Bitwise XOR B and C (op is ignored)
        self.B=self.B^self.C
        self.pointer+=2

    def out(self,op): #prog_out mod 8
        self.prog_out.append(self.combo(op)%8)
        self.pointer+=2

    def bdv(self,op): #Divide A, store in B
        self.B=self.A//2**self.combo(op)
        self.pointer+=2

    def cdv(self,op): #Divide A, store in C
        self.C=self.A//2**self.combo(op)
        self.pointer+=2

    def run_step(self): #Run next step
        self.instructions[self.program[self.pointer]](self.program[self.pointer+1])

    def run_program_p1(self):
        while self.pointer in range(len(self.program)-1):
            self.run_step()
        return(','.join([str(x) for x in self.prog_out]))
    
    def run_program(self):
        while self.pointer in range(len(self.program)-1):
            self.run_step()
        return([str(x) for x in self.prog_out])
    
def check_self(): #Check if program prog_outs itself
    program=re.findall(r'(\d+)',input[-1])
    
    zeroes = ['0' for i in range(16)]

    frontier = []
    initial = (zeroes, 0)
    frontier.append(initial)

    while len(frontier)>0:
        state, digit = frontier.pop()

        for d in reversed(range(8)):
            # make a new base8 candidate
            new = state.copy()
            new[digit] = str(d)
            octal = f"0o{''.join(new)}"
            # convert to base 10 to input to register A
            A = int(octal, 8)    

            # run computer and test
            prog_out=Computer(input,A).run_program()
            match = prog_out[-digit-1] == program[-digit-1]

            # found it, return!
            if prog_out == program:
                return(A)

            # not found yet but match at the next octal digit, so advance
            if match:
                new_state = (new.copy(), digit + 1)
                frontier.append(new_state)
    print('No solution found')

#Part 1
computer=Computer(input)
print(computer.run_program_p1())

#Part 2
print(check_self())