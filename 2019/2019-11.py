#Advent of Code 2019 Day 11

from collections import deque
from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-11.txt')
contents = f.read()
code = [int(x) for x in contents.split(',')]

def get_digit(number, n):
    return number // 10**n % 10

class Computer():
    
    def __init__(self,code): #Initialise a Computer instance
        self.code=defaultdict(int) #Convert code to defaultdict to allow pointer to reach new memory
        for i in range(len(code)):
            self.code[i]=code[i]
        self.point=0 #Position of code pointer
        self.step=0 #Number of steps run
        self.input=None #Input
        self.output=deque() #Queue of outputs
        self.complete=False
        self.relativeBase=0
        
    def __str__(self): #Print current computer state
        ret='Step: '+str(self.step)+' Pointer: '+str(self.point)+'\n'+str(self.code)
        return(ret)
    
    def setInput(self,input): #Update value of input
        self.input=input

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
                self.code[dest]=self.input
            
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

class HullBot(): #Hull-painting robot
    
    def __init__(self,code):
        self.brain=Computer(code) #Load robot with intcode
        self.hullMap=defaultdict(int) #Map of coordinates where 0=black, 1=white
        self.painted=set() #Set of coordinates that have been painted at least once
        self.pos=complex(0,0) #Bot starts at origin
        self.dir=complex(0,1) #Bot starts facing north
    
    def setWhite(self): #Set current position to white (for part 2)
        self.hullMap[complex(0,0)]=1
    
    def __str__(self):
        font={0:' ', 1:'#'} #Convert 0 and 1 to 'black' and 'white'
        minX=int(min(self.painted,key=lambda x:x.real).real)
        minY=int(min(self.painted,key=lambda x:x.imag).imag)
        maxX=int(max(self.painted,key=lambda x:x.real).real)
        maxY=int(max(self.painted,key=lambda x:x.imag).imag)
        ret=''
        for y in range(maxY,minY-1,-1):
            for x in range(minX,maxX+1):
                ret+=font[self.hullMap[complex(x,y)]]
            if y>=minY-1:
                ret+='\n'
        return(ret)
                
    def runBot(self): #Run hull robot program
        while not self.brain.complete:
            #Determine colour of current position to set input value
            self.brain.setInput(self.hullMap[self.pos])
            #Run code to produce 2 output values
            while len(self.brain.output)<2 and not self.brain.complete:
                self.brain.runStep()
            if self.brain.complete:
                break
            #print('PAINTING AT '+str(self.pos))
            #Paint current position based on output value 1
            self.hullMap[self.pos]=self.brain.getOutput()
            #Add painted position to painted set
            self.painted.add(self.pos)
            #Turn robot in place based on output value 2
            turn=self.brain.getOutput()
            if turn==0: #Left 90 degrees
                self.dir*=complex(0,1)
            elif turn==1: #Right 90 degrees
                self.dir*=complex(0,-1)
            #Move 1 step forward
            self.pos+=self.dir
        return(len(self.painted))
        
def solveA(code):
    bot=HullBot(code)
    nPainted=bot.runBot()
    print(bot)
    return(nPainted)

retA=solveA(code)
        
def solveB(code):
    bot=HullBot(code)
    bot.setWhite()
    bot.runBot()
    print(bot)

solveB(code)        
        
        