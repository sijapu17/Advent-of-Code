#Advent of Code 2017 Day 18

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-18.txt')
contents = f.read()
input = contents.splitlines()
#input=['mul p 17']
#input=['set a 3','set b 6','snd 5','rcv c','snd 4','rcv a']

class Duet(): #List of instructions with associated registries
    
    def __init__(self,inlist):
        self.reg={} #Dictionary of registries
        self.instrs={} #Numbered dictionary of instructions
        self.iLen=len(inlist)
        self.pointer=0 #Next instruction to run
        self.sound=None #Most recent sound played
        self.rcv=False #Has sound been recovered yet
        n=0
        for ins in inlist: #Find all required registry names
            a=ins.split(' ')[1]
            if a.isalpha() and a not in self.reg:
                self.reg[a]=0
            b=ins.split(' ')[-1]
            if b.isalpha() and b not in self.reg:
                self.reg[b]=0
            self.instrs[n]=ins
            n+=1
            
    def runNext(self): #Run next instruction
        ins=self.instrs[self.pointer]
        print(ins)
        cat=ins.split(' ')[0] #Category of instruction
        if cat=='snd': #Sound instruction
            val=ins.split(' ')[1]
            if val.isalpha():
                self.sound=self.reg[val]
            else:
                self.sound=int(val)
            self.pointer+=1
        elif cat=='set': #Set instruction
            r=ins.split(' ')[1]
            val=ins.split(' ')[2]
            if val.isalpha():
                self.reg[r]=int(self.reg[val])
            else:
                self.reg[r]=int(val)
            self.pointer+=1
        elif cat=='add': #Add instruction
            r=ins.split(' ')[1]
            val=ins.split(' ')[2]
            if val.isalpha():
                self.reg[r]+=self.reg[val]
            else:
                self.reg[r]+=int(val)
            self.pointer+=1
        elif cat=='mul': #Multiply instruction
            r=ins.split(' ')[1]
            val=ins.split(' ')[2]
            if val.isalpha():
                self.reg[r]=self.reg[r]*self.reg[val]
            else:
                self.reg[r]=self.reg[r]*int(val)
            self.pointer+=1
        elif cat=='mod': #Remainder instruction
            r=ins.split(' ')[1]
            val=ins.split(' ')[2]
            if val.isalpha():
                self.reg[r]=self.reg[r]%self.reg[val]
            else:
                self.reg[r]=self.reg[r]%int(val)
            self.pointer+=1            
        elif cat=='rcv': #Recover sound instruction
            val=ins.split(' ')[1]
            if val.isalpha():
                if self.reg[val]!=0:
                    self.rcv=True
            else:
                if val!=0:
                    self.rcv=True
            self.pointer+=1
        elif cat=='jgz': #Jump instruction
            val1=ins.split(' ')[1]
            val2=ins.split(' ')[2]
            if val1.isalpha():
                jump=(self.reg[val1]>0)
            else:
                jump=(int(self.val1)>0)
            if val2.isalpha():
                dist=self.reg[val2]
            else:
                dist=int(val2)
            if jump: #Only jump if val1>0
                self.pointer+=dist
            else:
                self.pointer+=1            
            
def solveA(input):
    duet=Duet(input)
    while ((0<=duet.pointer<duet.iLen) and not duet.rcv):
        duet.runNext()
    return(duet.sound)

retA=solveA(input)