#Advent of Code 2016 Day 23

import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-23b.txt')
contents = f.read()
input = contents.splitlines()

class Computer(): #List of instructions with associated registries
    
    def __init__(self,inlist):
        self.reg={} #Dictionary of registries
        self.instrs={} #Numbered dictionary of instructions
        self.iLen=len(inlist)
        self.pointer=0 #Next instruction to run
        n=0
        for i in inlist:
            self.instrs[n]=i
            n+=1
        for l in 'abcd': #Find all required registry names
            self.reg[l]=0
        #self.reg['a']=7  #Part 1
        self.reg['a']=12 #Part 2
        
    def toggle(self,ins):
        nArgs=len(ins.split(' '))-1
        cat=ins.split(' ')[0] #Category of instruction
        val1=ins.split(' ')[1]
        if nArgs==1:
            if cat=='inc':
                ret='dec '+val1
            else:
                ret='inc '+val1
        elif nArgs==2:
            val2=ins.split(' ')[2]
            if cat=='jnz':
                ret='cpy '+val1+' '+val2
            else:
                ret='jnz '+val1+' '+val2
        return(ret)
    def runNext(self): #Run next instruction
        ins=self.instrs[self.pointer]
        #print(str(self.pointer))
        #print(ins)
        cat=ins.split(' ')[0] #Category of instruction
        if cat=='cpy': #Copy instruction
            val=ins.split(' ')[1]
            r=ins.split(' ')[2]
            if r.isalpha():
                if val.isalpha():
                    self.reg[r]=int(self.reg[val])
                else:
                    self.reg[r]=int(val)
            self.pointer+=1
        elif cat=='inc': #Increment instruction
            r=ins.split(' ')[1]
            if r.isalpha():
                self.reg[r]+=1
            self.pointer+=1
        elif cat=='dec': #Decrement instruction
            r=ins.split(' ')[1]
            if r.isalpha():
                self.reg[r]-=1
            self.pointer+=1
        elif cat=='add': #Add instruction
            r1=ins.split(' ')[1]
            r2=ins.split(' ')[2]
            self.reg[r2]+=self.reg[r1]
            self.pointer+=1
        elif cat=='mul': #Multiply instruction
            r1=ins.split(' ')[1]
            r2=ins.split(' ')[2]
            self.reg[r2]*=self.reg[r1]
            self.pointer+=1
        elif cat=='nop': #Skip instruction
            self.pointer+=1
        elif cat=='tgl': #Toggle instruction
            val=ins.split(' ')[1]
            if val.isalpha():
                r=int(self.reg[val])
            else:
                r=int(val)
            target=self.pointer+r
            if 0<=target<self.iLen:
                in2tgl=self.instrs[target] #Pick out instruction to toggle
                self.instrs[self.pointer+r]=self.toggle(in2tgl)
            self.pointer+=1
        elif cat=='jnz': #Jump instruction
            val1=ins.split(' ')[1]
            val2=ins.split(' ')[2]
            if val1.isalpha():
                jump=(self.reg[val1]!=0)
            else:
                jump=(int(val1)!=0)
            if val2.isalpha():
                dist=self.reg[val2]
            else:
                dist=int(val2)
            if jump!=0: #Only jump if val1!=0
                self.pointer+=dist
            else:
                self.pointer+=1            
            
def solveA(input):
    computer=Computer(input)
    i=0
    while (0<=computer.pointer<computer.iLen):
        if i%100000==1:
            print('Step '+str(i))
        computer.runNext()
        i+=1
    return(computer.reg)

retA=solveA(input)