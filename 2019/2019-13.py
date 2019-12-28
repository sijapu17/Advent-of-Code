#Advent of Code 2019 Day 13

from collections import deque
from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-13.txt')
contents = f.read()
code = [int(x) for x in contents.split(',')]

def get_digit(number, n):
    return number // 10**n % 10

def get_key(dict,val): 
    for key, value in dict.items(): 
        if val == value: 
            return key
            
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
    
    def setAddress(self,pos,val): #Set position pos to value val
        self.code[pos]=val
    
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

class Arcade(): #Arcade cabinet
    
    def __init__(self,code):
        self.brain=Computer(code) #Load arcade with intcode
        self.screen=defaultdict(int) #Map of coordinates where 0=empty, 1=wall, 2=block, 3=paddle, 4=ball
    
    def __str__(self):
        font={0:' ', 1:'#', 2:'X', 3:'-', 4:'O'} #Convert numbers to object
        #Find bounds of screen
        minX=0
        minY=int(min(self.screen,key=lambda x:x.imag).imag)
        maxX=int(max(self.screen,key=lambda x:x.real).real)
        maxY=int(max(self.screen,key=lambda x:x.imag).imag)
        ret=''
        score=''
        for y in range(minY,maxY+1):
            for x in range(minX,maxX+1):
                #Score is stored in position (-1,0)
                if (x,y)==(-1,0):
                    score=str(self.screen[complex(x,y)])
                #Convert tile from number to ASCII representation
                else:
                    ret+=font[self.screen[complex(x,y)]]
            if y>=minY-1:
                ret+='\n'
        return(score+'\n'+ret)
    
    def getLocation(self,tile): #Return location of tile
        return(get_key(self.screen,tile))
    
    def bestPaddleDirection(self): #Determine best direction to move paddle to get it closer to ball
        paddle=self.getLocation(3)
        if type(paddle)==complex:
            paddleX=paddle.real
        else:
            paddleX=-99
        ball=self.getLocation(4)
        if type(ball)==complex:
            ballX=ball.real
        else:
            ballX=-99            
        if paddleX>ballX: #Move paddle left
            return(-1)
        if paddleX<ballX: #Move paddle right
            return(1)
        else: #Don't move paddle
            return(0)
        
    def loadGame(self): #Run code to load starting screen
        nBlocks=0 #Count number of block tiles produced
        while not self.brain.complete:
            #Run code to produce 3 output values
            while len(self.brain.output)<3 and not self.brain.complete:
                self.brain.runStep()
            if self.brain.complete:
                break
            #Get pair of coordinates from first two outputs
            xPos=self.brain.getOutput()
            yPos=self.brain.getOutput()
            #Add tile to screen as specified by third output
            tile=self.brain.getOutput()
            self.screen[complex(xPos,yPos)]=tile
            if tile==2:
                nBlocks+=1
        return(nBlocks)
    
    def runGame(self): #Run code to play game
        self.brain.setAddress(0,2) #Set address 0 to value 2 to add quarters
        while not self.brain.complete:
            #Determine input instruction to be given, based on relative position of paddle and ball
            self.brain.setInput(self.bestPaddleDirection())
            #Run code to produce 3 output values
            while len(self.brain.output)<3 and not self.brain.complete:
                self.brain.runStep()
            if self.brain.complete:
                break
            #Get pair of coordinates from first two outputs
            xPos=self.brain.getOutput()
            yPos=self.brain.getOutput()
            #Add tile to screen as specified by third output
            tile=self.brain.getOutput()
            self.screen[complex(xPos,yPos)]=tile
        score=self.screen[complex(-1,0)] #Score is stored in position (-1,0)
        return(score)
    
def solveA(code):
    arcade=Arcade(code)
    nBlocks=arcade.loadGame()
    print(arcade)
    return(nBlocks)

#retA=solveA(code)
        
def solveB(code):
    arcade=Arcade(code)    
    score=arcade.runGame()
    print(arcade)
    return(score)

retB=solveB(code)        
        
        