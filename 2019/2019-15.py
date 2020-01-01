#Advent of Code 2019 Day 15

from collections import deque
from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-15.txt')
contents = f.read()
code = [int(x) for x in contents.split(',')]

def get_digit(number, n):
    return number // 10**n % 10

def get_key(dict,val): 
    for key, value in dict.items(): 
        if val == value: 
            return key
            
class Computer():
    
    def __init__(self,code,point=0): #Initialise a Computer instance
        self.code=defaultdict(int) #Convert code to defaultdict to allow pointer to reach new memory
        for i in range(len(code)):
            self.code[i]=code[i]
        self.point=point #Position of code pointer
        self.step=0 #Number of steps run
        self.input=None #Input
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
                #print('INPUT: '+str(self.input))
            
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

class Node(): #BFS node consisting of droid and next direction to try
    
    def __init__(self,droid,nextDir,pos,steps):
        self.droid=droid
        self.nextDir=nextDir
        self.pos=pos
        self.steps=steps
        
    def __str__(self):
        return(self.droid.__str__()+' '+self.nextDir+' '+str(self.pos)+' '+str(self.steps)+' steps')
        
class System(): #Top-level class which runs BFS queue of droid instances to create map and search for oxygen system
    
    def __init__(self,code):
        self.code=code #Code which droids will run
        self.map=defaultdict(lambda:' ') #Map of coordinates where ' '=empty/unknown, '#'=wall, '.'=hallway, 'O'=oxygen system
        self.queue=deque() #Queue of Computer states trying movement in different directions
        self.complexDirs={'N':complex(0,1),'S':complex(0,-1),'W':complex(-1,0),'E':complex(1,0)}
    
    def __str__(self):
        #Find bounds of map
        minX=int(min(self.map,key=lambda x:x.real).real)
        minY=int(min(self.map,key=lambda x:x.imag).imag)
        maxX=int(max(self.map,key=lambda x:x.real).real)
        maxY=int(max(self.map,key=lambda x:x.imag).imag)
        ret=''
        for y in range(minY,maxY+1):
            for x in range(minX,maxX+1):
                if (x,y)==(0,0):
                    ret+='X' #Mark origin
                else:
                    ret+=self.map[complex(x,y)]
            if y>=minY-1:
                ret+='\n'
        return(ret)
    
    def runBFS(self): #Run BFS queue from origin
        droid=Droid(self.code)
        nodesExplored=0
        for d in ('N','S','W','E'):
            node=Node(droid.__copy__(),d,complex(0,0),0) #Create nodes for droid travelling in each direction from origin
            self.queue.appendleft(node)
        while len(self.queue)>0:
            node=self.queue.pop() #Pop next node from queue
            nodesExplored+=1
            #print(node)
            newPos=node.pos+self.complexDirs[node.nextDir] #Coordinates of attempted new position
            steps=node.steps+1
            if self.map[newPos]==' ': #Only explore node if new position is unknown
                status=node.droid.move(node.nextDir) #Attempt to move droid in given direction
                #print(str(status))
                if status==0: #If droid hit a wall, mark on map and discard node
                    self.map[newPos]='#'
                elif status==1: #If droid moved into new hallway, create new nodes in each direction to explore
                    self.map[newPos]='.'
                    for d in ('N','S','W','E'):
                        node=Node(node.droid.__copy__(),d,newPos,steps) #Create nodes for droid travelling in each direction from origin
                        self.queue.appendleft(node)
                elif status==2: #If oxygen system is found, print map and return number of steps away
                    self.map[newPos]='O'
                    return(steps)
        

class Droid(): #Repair droid
    
    def __init__(self,code,p=0):
        self.brain=Computer(code,point=p) #Load droid with intcode
        self.dirCode={'N':1,'S':2,'W':3,'E':4}
        
    def __str__(self):
        return('Droid: '+self.brain.__str__())
        
    def __copy__(self): #Create a copy of droid for BFS
        brainState=self.brain.saveState()
        droid=Droid(brainState['code'],p=brainState['point'])
        return(droid)
            
    def move(self,dir): #Input direction value to droid brain, and output status value
        self.brain.setInput(self.dirCode[dir]) #Convert compass direction to intcode value
        while len(self.brain.output)<1: #Run intcode until output produced
            self.brain.runStep()
        status=self.brain.getOutput()
        return(status)
    
def solveA(code):
    system=System(code)
    nSteps=system.runBFS()
    print(system)
    return(nSteps)

retA=solveA(code)     
        
        