#Advent of Code 2019 Day 5

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-05.txt')
contents = f.read()
code = [int(x) for x in contents.split(',')]

def get_digit(number, n):
    return number // 10**n % 10

class Computer():
    
    def __init__(self,code,ID): #Initialise a Computer instance
        self.code=code #Input code
        self.ID=ID #Input ID
        self.point=0 #Position of code pointer
        self.step=0 #Number of steps run
        self.complete=False
        
    def __str__(self): #Print current computer state
        ret='Step: '+str(self.step)+' Pointer: '+str(self.point)+'\n'+str(self.code)
        return(ret)
        
    def halt(self): #Set program state to complete when halt code is found
        print('PROGRAM HALTING')
        print(self)
        self.complete=True
        return(self.code[0])
    
    def runProg(self):
        #Run steps until halt is reached
        while self.complete==False:
            #if self.step%100==1:
            #    print('Step '+str(self.step))
            #print(self)
            self.runStep()
        return(self.code[0]) #Return number in position 0

    def runStep(self):
        print(self.step)
        jumped=False
        op=self.code[self.point]
        if op==99: #Halt instruction
            self.halt()
        else: #Decode instruction
            opS=str(op)
            opcode=int(opS[-2:]) #Collect last 2 digits of instruction as opcode
            if opcode in (1,2,7,8):
                nParams=3
            elif opcode in (3,4):
                nParams=1
            elif opcode in (5,6):
                nParams=2
            else:
                print('Invalid operator '+str(opcode)+' at position '+str(self.point))
            #print(self.code[self.point:self.point+nParams+1])

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
                    #print('Add Params='+str(params))
                    res=params[0]+params[1]
                    #print('Add Res='+str(res))
                elif opcode==2: #Multiplication
                    res=params[0]*params[1]
                self.code[dest]=res #Assign calculated result to specified destination
                
            elif opcode==3: #Input
                dest=self.code[self.point+1]
                self.code[dest]=self.ID
            
            elif opcode==4: #Output
                result=params[0]
                print('OUTPUT: '+str(result))
                
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
            
def solveB(code):
    comp=Computer(code,5)
    return(comp.runProg())
    
retB=solveB(code)
            

                