#Advent of Code 2019 Day 25

from collections import deque
from collections import defaultdict
from itertools import combinations

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-25.txt')
contents = f.read()
code = [int(x) for x in contents.split(',')]

g = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-25 directions.txt')
contents = g.read()
directions = contents.splitlines()

def get_digit(number, n):
    return number // 10**n % 10

def get_key(dict,val): 
    for key, value in dict.items(): 
        if val == value: 
            return key
        
def firstDigit(s): #Return position of first digit in string
    for i in range(len(s)):
        if s[i].isdigit():
            return(i)
    return(-1)
            
class Computer():
    
    def __init__(self,code,point=0): #Initialise a Computer instance
        self.code=defaultdict(int) #Convert code to defaultdict to allow pointer to reach new memory
        for i in range(len(code)):
            self.code[i]=code[i]
        self.point=point #Position of code pointer
        self.step=0 #Number of steps run
        self.input=deque() #Queue of inputs
        self.output=deque() #Queue of outputs
        self.complete=False
        self.relativeBase=0
        self.inputString='' #Text that has been input
        
    def __str__(self): #Print current computer state
        ret='Step: '+str(self.step)+' Pointer: '+str(self.point)+'\n'+str(self.codeChecksum())
        return(ret)
    
    def codeChecksum(self): #Return a checksum of the code, to compare whether two instances are the same
        count=0
        for k,v in self.code.items():
            count+=(k*v)
        return(count)
    
    def saveState(self): #Save current program state (code and pointer) to a dict, which can be used to create a new Computer object at the saved state
        return({'code':self.code.copy(),'point':self.point})    
    
    def setAddress(self,pos,val): #Set position pos to value val
        self.code[pos]=val
    
    def loadInputList(self,lst): #Load a list of input values (int or ASCII char) into input queue
        for x in lst:
            self.setInput(x)
    
    def setInput(self,input): #Update value of input
        if type(input)==str and len(input)==1:
            input=ord(input) #Convert ASCII value to integer
        self.input.appendleft(input) 
        
    def getInput(self): #Get next input value
        return(self.input.pop())

    def getOutput(self): #Pop oldest output value from queue
        return(self.output.pop())
        
    def halt(self): #Set program state to complete when halt code is found
        self.complete=True
        #print('COMPLETED')
        return('Completed')

    def runProg(self):
        #Run steps until halt is reached
        while self.complete==False:
            self.runStep()
        return(self.code[0]) #Return number in position 0
    
    def runStep(self):
        jumped=False
        op=self.code[self.point]
        opS=str(op)
        opcode=int(opS[-2:]) #Collect last 2 digits of instruction as opcode
        if opcode==99: #Halt instruction
            self.halt()
        else: #Decode instruction, determine whether parameters are [R]ead or [W]rite
            if opcode in (1,2,7,8):
                nParams=3
                pType=['R','R','W']
            elif opcode in (3,4,9):
                nParams=1
                if opcode in (4,9):
                    pType=['R']
                elif opcode==3:
                    pType=['W']
            elif opcode in (5,6):
                nParams=2
                pType=['R','R']
            else:
                print('Invalid operator '+str(opcode)+' at position '+str(self.point))

            pModes=[] #Fill with 0 (position mode) or 1 (immediate mode) or 2 (relative mode)
            for i in range(nParams):
                pModes.append(get_digit(op,i+2))
            params=[]
            for i in range(nParams):
                val=self.code[self.point+i+1]
                if pModes[i]==0: #Position mode
                    if pType[i]=='R': #Read type
                        params.append(self.code[val])
                    elif pType[i]=='W': #Write type
                        params.append(val)
                elif pModes[i]==1: #Immediate mode - read type only
                    params.append(val)
                elif pModes[i]==2: #Relative mode
                    if pType[i]=='R': #Read type
                        params.append(self.code[val+self.relativeBase])
                    elif pType[i]=='W': #Write type
                        params.append(val+self.relativeBase)
                    
            if opcode in (1,2):
                dest=params[2]
                if opcode==1: #Addition
                    res=params[0]+params[1]
                elif opcode==2: #Multiplication
                    res=params[0]*params[1]
                self.code[dest]=res #Assign calculated result to specified destination
                
            elif opcode==3: #Input
                dest=params[0]
                if len(self.input)==0: #Accept typed user input
                    userIn=input("")
                    listIn=list(userIn)
                    listIn.append('\n')
                    self.loadInputList(listIn)
                inp=self.getInput()
                if inp==-999:
                    return()
                self.code[dest]=inp
                #Print ASCII code that has been input
                if inp==10:
                    print(self.inputString)
                    self.inputString=''
                else:
                    self.inputString+=chr(inp)
            
            elif opcode==4: #Output
                result=params[0]
                self.output.appendleft(result) #Add to output queue
                #print('OUTPUT: '+str(result))
                
            elif opcode in (5,6): #Jump instructions
                test=params[0]
                
                if (opcode==5 and test!=0) or (opcode==6 and test==0):
                    jumped=True
                    self.point=params[1]
                    
            elif opcode in (7,8): #Compare instructions
                dest=params[2]
                if (opcode==7 and params[0]<params[1]) or (opcode==8 and params[0]==params[1]):
                    self.code[dest]=1
                else:
                    self.code[dest]=0
                    
            elif opcode==9: #Change relative base
                self.relativeBase+=params[0]
                    
            if not jumped:
                self.point+=nParams+1 #Move to next instruction, unless already jumped
            self.step+=1 #Increment step count


class System(): #Springdroid system
    
    def __init__(self,code,directions):
        self.brain=Computer(code)
        for instr in directions: #load commands
            self.brain.loadInputList(instr)
            self.brain.loadInputList('\n')
            
    def runSystem(self): #Run system
        line='' #Current output line
        while not self.brain.complete:
            ret=self.brain.runStep() #Run intcode until halt
            if self.brain.complete:
                return(ret)
            if len(self.brain.output)==1:
                out=self.brain.getOutput()
                if out==10: #If newline is outputted, print current line
                    print(line)
                    line=''
                elif out in range(32,128): #Add ASCII characters to current line
                    line+=chr(out)
                else: #If number is large, return it
                    return(out)

def solve(code,directions):
    items=('sand','astronaut ice cream','festive hat','boulder','prime number','mug','mutex')
    system=System(code,directions) #Manually explored maze to arrive at checkpoint with all items on the floor
    for n in range(1,5): #Try combinations of items
        for list in combinations(items,n):
            for item in list:
                system.brain.loadInputList('take ')
                system.brain.loadInputList(item)
                system.brain.loadInputList('\n')
            system.brain.loadInputList('east\n')
            for item in list:
                system.brain.loadInputList('drop ')
                system.brain.loadInputList(item)
                system.brain.loadInputList('\n')
    system.runSystem()

retA=solve(code,directions)

