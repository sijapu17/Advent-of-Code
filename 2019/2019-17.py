#Advent of Code 2019 Day 17

import math
from collections import deque
from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-17.txt')
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


class System(): #Scaffold system
    
    def __init__(self,code,p=0):
        self.code=code
        self.brain=Computer(self.code,point=p) #Load droid with intcode
        self.map=defaultdict(lambda:'.')
        self.loadMap()
    
    def __str__(self):
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
                ret3+=self.map[complex(x,y)]
            if y>=self.minY-1:
                ret3+='\n'
        return(ret1+'\n'+ret2+'\n'+ret3) 
    
    def loadMap(self): #Run program to display map
        i,j=0,0
        while not self.brain.complete:
            self.brain.runStep() #Run intcode until halt
            if len(self.brain.output)==1:
                tile=chr(self.brain.getOutput())
                if tile=='\n': #Newline
                    j+=1
                    i=0
                else:
                    self.map[complex(i,j)]=tile
                    i+=1
        #Find bounds of map
        self.minX=0
        self.minY=0
        self.maxX=int(max(self.map,key=lambda x:x.real).real)
        self.maxY=int(max(self.map,key=lambda x:x.imag).imag)
        
    def runRobot(self,cmprs): #Run cleaning robot
        self.brain=Computer(self.code) #Reset robot
        self.brain.setAddress(0,2) #Set address 0 to 2
        self.brain.loadInputList(cmprs)
        line='' #Current output line
        while not self.brain.complete:
            self.brain.runStep() #Run intcode until halt
            if len(self.brain.output)==1:
                out=self.brain.getOutput()
                if out==10: #If newline is outputted, print current line
                    print(line)
                    line=''
                elif out in range(32,128): #Add ASCII characters to current line
                    line+=chr(out)
                else: #If number is large, return it
                    return(out)
                    
        
    def traverseMap(self): #Generate sequence of L/R turns and movement distances for bot to traverse the full scaffold
        route=[]
        pos=get_key(self.map,'^') #Starting point of bot
        dir=complex(0,-1) #Bot starts facing in -ve Y direction
        legDist=0
        while True:
            if self.map[pos+dir]=='#': #If scaffold ahead, move onto it
                pos+=dir
                legDist+=1
            else: #If space ahead, end forward movement and try to turn left or right
                if legDist>0:
                    route.append(legTurn+str(legDist))
                legDist=0 #Reset forward distance
                if self.map[pos+dir*complex(0,-1)]=='#': #Try left turn
                    legTurn='L'
                    dir*=complex(0,-1)  
                elif self.map[pos+dir*complex(0,1)]=='#': #If no left turn available, try right turn
                    legTurn='R'
                    dir*=complex(0,1)
                else: #If dead end reached, end of route
                    return(route)
    
    def compressRoute(self,route): #Compress route into subroutines A, B and C
        #First, substitute each turn & move instruction with a number
        route1=''
        conversion={} #Keep track of which numbers have already been seen
        i=0
        for n in route:
            if n not in conversion:
                conversion[n]=str(i)
                i+=1
            route1+=conversion[n]
        convertBack={} #Create reverse dictionary to convert back later
        for k,v in conversion.items():
            convertBack[v]=k
        for i in range(1,6): #A could consist of up to 5 instructions, from start
            for j in range(1,6): #B could consist of up to 5 instructions from the first uncompressed position
                for k in range(1,6): #C could consist of up to 5 instructions from end
                    #print(route1)
                    strRoute=route1
                    subroutines={}
                    subroutines['a']=''.join(route1[:i]) #Candidate for A
                    subroutines['c']=''.join(route1[-k:]) #Candidate for C
                    strRoute=strRoute.replace(subroutines['a'],'A')
                    strRoute=strRoute.replace(subroutines['c'],'C')

                    p=firstDigit(strRoute) #Position of first uncompressed digit
                    beforeB=strRoute[:p+1] #Compressed section at start
                    offset=i*beforeB.count('A')+k*beforeB.count('C')
                    subroutines['b']=''.join(route1[offset:offset+j]) #Candidate for B
                    strRoute=strRoute.replace(subroutines['b'],'B')
                    #print('A='+subroutines['a'])
                    #print('B='+subroutines['b'])
                    #print('C='+subroutines['c'])
                    #print(strRoute+'\n')
                    if firstDigit(strRoute)==-1: #If no digits remain, full compression has been achieved
                        ret=[] #Output list of main routine followed by subroutines
                        for x in strRoute: #Main routines
                            ret.append(x)
                            ret.append(',')
                        ret.pop() #Remove last comma
                        ret.append('\n') #add newline
                        for i in 'abc': #Subroutines
                            for d in subroutines[i]:
                                step=convertBack[d] #Convert digit into step (e.g. 'R10')
                                for x in range(len(step)):
                                    ret.append(step[x])
                                    if x==0: #Insert comma after L/R instruction
                                        ret.append(',')
                                ret.append(',')
                            ret.pop() #Remove last comma
                            ret.append('\n') #add newline
                        ret.append('n') #Option to view continuous video feed
                        ret.append('\n') #add newline
                        return(ret) 
    
    def evaluateIntersections(self): #Sum up x*y coordinates of all intersections on map
        total=0
        for y in range(self.minY,self.maxY+1):
            for x in range(self.minX,self.maxX+1):
                if self.map[complex(x,y)]=='#': #Intersections must be on scaffold
                    if self.map[complex(x+1,y)]=='#' and self.map[complex(x-1,y)]=='#':
                        if self.map[complex(x,y+1)]=='#' and self.map[complex(x,y-1)]=='#':
                            print('Intersection at '+str(x)+','+str(y))
                            total+=(x*y)
        return(total)
    
def solveA(code):
    system=System(code)
    print(system)
    return(system.evaluateIntersections())

#retA=solveA(code)

def solveB(code):
    system=System(code)
    route=system.traverseMap() #Find full route from map
    cmprs=system.compressRoute(route) #Compress route into bot-readable form
    retB=system.runRobot(cmprs)
    return(retB)

retB=solveB(code)