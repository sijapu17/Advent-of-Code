#Advent of Code 2017 Day 23

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2017-23.txt')
contents = f.read()
input = contents.splitlines()

class Coproc(): #List of instructions with associated registries
    
    def __init__(self,inlist):
        self.reg={} #Dictionary of registries
        self.instrs={} #Numbered dictionary of instructions
        self.iLen=len(inlist)
        self.pointer=0 #Next instruction to run
        self.mults=0 #Count number of mults run
        n=0
        for i in inlist:
            self.instrs[n]=i
            n+=1
        for l in 'abcdefgh': #Find all required registry names
            self.reg[l]=0
            
    def runNext(self): #Run next instruction
        ins=self.instrs[self.pointer]
        #print(str(self.pointer))
        #print(ins)
        cat=ins.split(' ')[0] #Category of instruction
        if cat=='set': #Set instruction
            r=ins.split(' ')[1]
            val=ins.split(' ')[2]
            if val.isalpha():
                self.reg[r]=int(self.reg[val])
            else:
                self.reg[r]=int(val)
            self.pointer+=1
        elif cat=='sub': #Subtract instruction
            r=ins.split(' ')[1]
            val=ins.split(' ')[2]
            if val.isalpha():
                self.reg[r]-=self.reg[val]
            else:
                self.reg[r]-=int(val)
            self.pointer+=1
        elif cat=='mul': #Multiply instruction
            r=ins.split(' ')[1]
            val=ins.split(' ')[2]
            if val.isalpha():
                self.reg[r]=self.reg[r]*self.reg[val]
            else:
                self.reg[r]=self.reg[r]*int(val)
            self.pointer+=1
            self.mults+=1
        elif cat=='jnz': #Jump instruction
            val1=ins.split(' ')[1]
            val2=ins.split(' ')[2]
            if val1.isalpha():
                jump=(self.reg[val1]!=0)
            else:
                jump=(int(val1)!=0)
            if val2.isalpha():
                dist=self.reg[val2]
            else:
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
    return(coproc.mults)

retA=solveA(input)