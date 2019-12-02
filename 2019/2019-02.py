#Advent of Code 2019 Day 2

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-02.txt')
contents = f.read()
input = [int(x) for x in contents.split(',')]

class Computer():
    
    def __init__(self,code): #Initialise a Computer instance
        self.code=code #Input program
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
        op=self.code[self.point]
        if op==99: #Halt instruction
            self.halt()
        else:
            x=(self.code[self.code[self.point+1]],self.code[self.code[self.point+2]])
            dest=self.code[self.point+3]
            if op==1: #Addition
                res=x[0]+x[1]
            elif op==2: #Multiplication
                res=x[0]*x[1]
            else:
                print('Invalid operator '+str(op)+' at position '+str(self.point))
            self.code[dest]=res #Assign calculated result to specified destination
            self.point+=4 #Move to next instruction - this may need to change in future if different-length instructions are added
            self.step+=1 #Increment step count
            
def solveA(input):
    input[1]=12
    input[2]=2
    #input=[1,9,10,3,2,3,11,0,99,30,40,50]
    comp=Computer(input)
    return(comp.runProg())
    
#retA=solveA(input)
            
def solveB(input):
    for n in range(100):
        for v in range(100):
            mem=input[:]
            mem[1]=n
            mem[2]=v
            print('n='+str(n)+', v='+str(v))
            comp=Computer(mem)
            if comp.runProg()==19690720:
                print('n='+str(n)+', v='+str(v))
                return(100*n+v)
    
retB=solveB(input) 
                