#Advent of Code 2015 Day 23

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-23.txt')
contents = f.read()
input = contents.splitlines()

class Coproc(): #List of instructions with associated registries
    
    def __init__(self,inlist):
        self.reg={} #Dictionary of registries
        self.instrs={} #Numbered dictionary of instructions
        self.iLen=len(inlist)
        self.pointer=0 #Next instruction to run
        n=0
        for i in inlist:
            self.instrs[n]=i.replace(',','')
            n+=1
        for l in 'ab': #Find all required registry names
            self.reg[l]=0
            
    def runNext(self): #Run next instruction
        ins=self.instrs[self.pointer]
        #print(str(self.reg))
        #print('i='+str(self.pointer))
        #print(ins)
        cat=ins.split(' ')[0] #Category of instruction
        if cat=='hlf': #Halve instruction
            r=ins.split(' ')[1]
            self.reg[r]=int(self.reg[r])/2
            self.pointer+=1
        elif cat=='tpl': #Triple instruction
            r=ins.split(' ')[1]
            self.reg[r]=int(self.reg[r])*3
            self.pointer+=1
        if cat=='inc': #Increment instruction
            r=ins.split(' ')[1]
            self.reg[r]=int(self.reg[r])+1
            self.pointer+=1
        elif cat=='jmp': #Jump instruction
            val1=ins.split(' ')[1]
            dist=int(val1)
            self.pointer+=dist
        elif cat=='jio': #Jump If One instruction
            val1=ins.split(' ')[1]
            val2=ins.split(' ')[2]
            #print(self.reg)
            jump=(self.reg[val1]==1)
            dist=int(val2)
            if jump: #Only jump if val1>0
                self.pointer+=dist
            else:
                self.pointer+=1            
        elif cat=='jie': #Jump If Even instruction
            val1=ins.split(' ')[1]
            val2=ins.split(' ')[2]
            jump=(self.reg[val1]%2==0)
            dist=int(val2)
            if jump: #Only jump if val1>0
                self.pointer+=dist
            else:
                self.pointer+=1
                
def solveA(input):
    coproc=Coproc(input)
    i=0
    while (0<=coproc.pointer<coproc.iLen):
        if i%1000==1:
            print('Step '+str(i))
        coproc.runNext()
    return(coproc.reg)
    #return(coproc)

retA=solveA(input)