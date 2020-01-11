#Advent of Code 2019 Day 19

import math
from collections import deque
from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-19.txt')
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


class System(): #Drone deployment system
    
    def __init__(self,code,p=0):
        self.code=code
        self.map=defaultdict(lambda:'.')
    
    def __str__(self):
        #Find bounds of map
        font={1:'#',0:'.'}
        self.minX=0
        self.minY=0
        self.maxX=int(max(self.map,key=lambda x:x.real).real)
        self.maxY=int(max(self.map,key=lambda x:x.imag).imag)
        ret1='  '
        ret2='  '
        ret3=''
        for x in range(self.maxX+1):
            if x%10==0: #Create tens row at top
                ret1+=str(math.floor(abs(x)/10%10))
            else:
                ret1+=' '
            ret2+=str(abs(x)%10) #Create units row at top
        for y in range(self.maxY+1):
            if y%10==0:
                ret3+=str(math.floor(abs(y)/10%10)) #Create tens column going down
            else:
                ret3+=' '
            ret3+=str(abs(y)%10) #Create units column going down
            for x in range(self.maxX+1):
                ret3+=font[self.map[complex(x,y)]]
            if y>=self.minY-1:
                ret3+='\n'
        return(ret1+'\n'+ret2+'\n'+ret3) 
    
    def scanArea(self,X,Y): #Run program to scan area and count how many points are affected by beam 
        count=0
        for j in range(Y):
            print('Y='+str(j))
            for i in range(X):
                self.brain=Computer(self.code) #Load drone with intcode
                self.brain.loadInputList([i,j])
                while not self.brain.complete:
                    self.brain.runStep() #Run intcode until halt
                    if len(self.brain.output)==1:
                        point=self.brain.getOutput()
                        self.map[complex(i,j)]=point
                        count+=point #Add 1 to count if beam is active in location
                        break
        return(count)
    
    def inBeam(self,i,j,): #Check a single point a return Boolean of whether beam is active
        self.brain=Computer(self.code) #Load drone with intcode
        self.brain.loadInputList([i,j])
        while not self.brain.complete:
            self.brain.runStep() #Run intcode until halt
            if len(self.brain.output)==1:
                return(self.brain.getOutput()==1)
                    
def solveA(code):
    system=System(code)
    return(system.scanArea(50,50))

#retA=solveA(code)

def mapBeam(code,X,Y):
    system=System(code)
    system.scanArea(X,Y)
    print(system)
    
#mapBeam(code,50,33)

def solveB(code,size):
    #Point (x,y) is the solution if it's the first point where (x+size-1,y) and (x,y+size-1) are both in the beam
    current=[0,0]
    system=System(code)
    while True:
        #Follow bottom edge of beam
        if system.inBeam(current[0],current[1]):
            if system.inBeam(current[0]+(size-1),current[1]-(size-1)):
                topLeft=[current[0],current[1]-(size-1)]
                print(str(10000*topLeft[0]+topLeft[1]))
                return(topLeft)
            else:
                current[0]+=1
                current[1]+=1
        else: #If current point is outside beam, move right until you are back in the beam
            current[0]+=1
        
retB=solveB(code,100)
