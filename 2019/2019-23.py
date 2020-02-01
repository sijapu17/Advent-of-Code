#Advent of Code 2019 Day 23

from collections import deque
from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-23.txt')
contents = f.read()
code = [int(x) for x in contents.split(',')]

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
    
    def __init__(self,code,id,point=0): #Initialise a Computer instance
        self.code=defaultdict(int) #Convert code to defaultdict to allow pointer to reach new memory
        for i in range(len(code)):
            self.code[i]=code[i]
        self.point=point #Position of code pointer
        self.step=0 #Number of steps run
        self.input=deque() #Queue of inputs
        self.output=deque() #Queue of outputs
        self.id=id
        self.paused=False
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
            self.loadInput(x)
    
    def loadInput(self,input): #Append value to input queue
        if type(input)==str and len(input)==1:
            input=ord(input) #Convert ASCII value to integer
        self.input.appendleft(input) 
    
    def getInput(self): #Get next input value
        return(self.input.pop())

    def getOutput(self): #Pop oldest output value from queue
        return(self.output.pop())
        
    def halt(self): #Set program state to complete when halt code is found
        self.complete=True
        self.paused=True
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
                if len(self.input)==0: #If no available input, move on to another computer
                    #print('No input')
                    self.loadInput(-1)
                    self.paused=True
                    return()
                inp=self.getInput()
                self.code[dest]=inp
                #print('INPUT: '+str(inp))
            
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


class System(): #NIC system
    
    def __init__(self,code):
        self.network={} #Dictionary of computers
        self.compQueue=deque() #Queue of which computer to run next
        for i in range(50):
            self.network[i]=Computer(code[:],i)
            self.network[i].loadInput(i)
            self.compQueue.appendleft(i)
    
    def runNICSystem(self): #Run system
        while True:
            active=self.network[self.compQueue.pop()] #Find next computer to run
            active.paused=False #Unpause active computer
            print('Running ID '+str(active.id))
            while not active.paused:
                active.runStep() #Run intcode until 3 outputs found, or pause
                if len(active.output)==3:
                    dest=active.getOutput() #First output value is the destination computer ID
                    if dest==255:
                        active.getOutput() #Uninterested in X value
                        return(active.getOutput()) #Return Y value
                    self.network[dest].loadInputList([active.getOutput(),active.getOutput()]) #Other two output values are input values for destination computer
                    self.compQueue.append(dest) #Put destination computer at front of queue
            self.compQueue.appendleft(active.id)
            
    def runNICNATSystem(self): #Run system
        idle=0 #Counter to recognise when whole system is idle
        sentByNAT=set() #Set of Y-values sent by NAT to computer 0
        while True:
            active=self.network[self.compQueue.pop()] #Find next computer to run
            active.paused=False #Unpause active computer
            #print('Running ID '+str(active.id))
            while not active.paused:
                active.runStep() #Run intcode until 3 outputs found, or pause
                if len(active.output)==3:
                    idle=0 #Packet is being transmitted so system is not idle
                    dest=active.getOutput() #First output value is the destination computer ID
                    if dest==255:
                        NAT=(active.getOutput(),active.getOutput()) #Remember latest packet sent to NAT
                    else:
                        self.network[dest].loadInputList([active.getOutput(),active.getOutput()]) #Other two output values are input values for destination computer
                        self.compQueue.append(dest) #Put destination computer at front of queue
            self.compQueue.appendleft(active.id)
            idle+=1
            if idle>55: #If system is idle, send last NAT value to computer 0
                print('SYSTEM IDLE')
                idle=0
                if NAT[1] in sentByNAT:
                    return(NAT[1]) #If NAT Y-value has been sent before, return it as final answer
                sentByNAT.add(NAT[1])
                self.network[0].loadInputList(NAT)
                self.compQueue.append(0) #Put computer 0 at front of queue
            
            
def solveA(code):
    system=System(code)
    return(system.runNICSystem())

retA=solveA(code)

def solveB(code):
    system=System(code)
    return(system.runNICNATSystem())

retB=solveB(code)
