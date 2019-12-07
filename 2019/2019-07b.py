#Advent of Code 2019 Day 7

from itertools import permutations
from collections import deque

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-07.txt')
contents = f.read()
code = [int(x) for x in contents.split(',')]

def get_digit(number, n):
    return number // 10**n % 10

class Computer():
    
    def __init__(self,code,id): #Initialise a Computer instance
        self.ID=id
        self.code=code #Input code
        self.point=0 #Position of code pointer
        self.step=0 #Number of steps run
        self.input=deque() #Queue of inputs
        self.output=deque() #Queue of outputs
        self.complete=False
        self.paused=False
        
    def __str__(self): #Print current computer state
        ret='Step: '+str(self.step)+' Pointer: '+str(self.point)+'\n'+str(self.code)
        return(ret)
    
    def addInput(self,input): #Push new inputs into queue
        self.input.appendleft(input)

    def popOutput(self): #Pop next output from queue
        if len(self.output)>0:
            return(self.output.pop())

    def popLastOutput(self): #Pop last output from queue
        if len(self.output)>0:
            return(self.output.pop())
    
    def halt(self): #Set program state to complete when halt code is found
        self.complete=True
        return(self.code[0])

    def runStep(self):
        jumped=False
        op=self.code[self.point]
        opS=str(op)
        opcode=int(opS[-2:]) #Collect last 2 digits of instruction as opcode
        if opcode==3 and len(self.input)==0: #If input is required but none is available, pause program to move to next thruster
            self.paused=True
            return
        if opcode==99: #Halt instruction
            self.halt()
        else: #Decode instruction
            if opcode in (1,2,7,8):
                nParams=3
            elif opcode in (3,4):
                nParams=1
            elif opcode in (5,6):
                nParams=2
            else:
                print('Invalid operator '+str(opcode)+' at position '+str(self.point))

            pModes=[] #Fill with 0 (position mode) or 1 (immediate mode)
            for i in range(nParams):
                pModes.append(get_digit(op,i+2))
            params=[]
            for i in range(nParams):
                if pModes[i]==0: #Position mode
                    params.append(self.code[self.code[self.point+i+1]])
                elif pModes[i]==1: #Immediate mode
                    params.append(self.code[self.point+i+1])
                    
            if opcode in (1,2):
                dest=self.code[self.point+3]
                if opcode==1: #Addition
                    res=params[0]+params[1]
                elif opcode==2: #Multiplication
                    res=params[0]*params[1]
                self.code[dest]=res #Assign calculated result to specified destination
                
            elif opcode==3: #Input
                dest=self.code[self.point+1]
                self.code[dest]=self.input.pop()
            
            elif opcode==4: #Output
                result=params[0]
                self.output.appendleft(result) #Add to output queue
                
            elif opcode in (5,6): #Jump instructions
                test=params[0]
                
                if (opcode==5 and test!=0) or (opcode==6 and test==0):
                    jumped=True
                    self.point=params[1]
                    
            elif opcode in (7,8): #Compare instructions
                dest=self.code[self.point+3]
                if (opcode==7 and params[0]<params[1]) or (opcode==8 and params[0]==params[1]):
                    self.code[dest]=1
                else:
                    self.code[dest]=0
                    
            if not jumped:
                self.point+=nParams+1 #Move to next instruction, unless already jumped
            self.step+=1 #Increment step count


class Thrusters(): #Array of 5 thrusters
    
    def __init__(self,code,perm):
        self.thrusters=[]
        self.pointer=0 #Pointer for active thruster
        self.complete=False
        for i in range(5): #Initialise thrusters with phase settings
            self.thrusters.append(Computer(code[:],i))
            self.thrusters[i].addInput(perm[i])
        self.thrusters[0].addInput(0)
        
    def runProcess(self):
        #Run steps until halt is reached
        while self.complete==False:
            self.runStep() 
        ret=self.thrusters[4].popLastOutput()
        return(ret) #Return latest output from thruster E   
        
    def runStep(self): #Run next step on active program
        current=self.thrusters[self.pointer]
        current.paused=False
        current.runStep()
        #If final thruster has completed, entire process has completed. Output last output from final thruster
        if current.complete and current.ID==4:
            self.complete=True
            return
        #If current thruster has paused awaiting input (or halted), move on to next thruster, transferring any queued data
        if current.paused or current.complete: 
            nxt=self.thrusters[(self.pointer+1)%5]
            for i in range(len(current.output)):
                nxt.addInput(current.popOutput())
            self.pointer=(self.pointer+1)%5
            


def solveB(code):
    mx=0 #Look for max result after thrusters have halted
    for p in permutations(range(5,10)):
        thrusters=Thrusters(code,p)
        output=thrusters.runProcess()
        if output>mx:
            mx=output
    return(mx)
        
retB=solveB(code)        