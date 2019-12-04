#Advent of Code 2017 Day 18 Part b

from collections import deque

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-18.txt')
contents = f.read()
input = contents.splitlines()
#input=['mul p 17']
#input=['snd 1','snd 2','snd p','rcv a','rcv b','rcv c','rcv d']

class Duet(): #Collection of twin Singlets which run together

    def __init__(self,inlist):
        self.singlets={}
        for i in range(2):
            self.singlets[i]=Singlet(self,inlist,i)
        self.queue=[deque(),deque()]
        self.send1=0 #Count number of values sent by singlet 1
            
    def getSinglet(self,id):
        return(self.singlets[id])
    
    def qAdd(self,id,e): #Add element to queue
        self.queue[id].append(e)
    
    def qGet(self,id): #Get element from queue
        return(self.queue[id].popleft())
    
    def runNext(self): #Choose which singlet to run next, and run one step
        status=[self.getSinglet(0).getStatus(),self.getSinglet(1).getStatus()]
        print(status)
        if (max(status)<0):
            return(self.send1) #Duet can run no longer
        elif status[0]>=status[1]: #Run singlet with longer status
            self.getSinglet(0).runNext()
        else:
            self.getSinglet(1).runNext()
            
        
        

class Singlet(): #List of instructions with associated registries
    
    def __init__(self,duet,inlist,id):
        self.duet=duet
        self.reg={} #Dictionary of registries
        self.instrs={} #Numbered dictionary of instructions
        self.iLen=len(inlist)
        self.pointer=0 #Next instruction to run
        self.id=id
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
        self.reg['p']=id #Set register p to program ID
            
    def runNext(self): #Run next instruction
        ins=self.instrs[self.pointer]
        print(str(self.id)+': '+ins)
        cat=ins.split(' ')[0] #Category of instruction
        if cat=='snd': #Send value instruction
            val=ins.split(' ')[1]
            if val.isalpha():
                self.duet.qAdd(1-self.id,self.reg[val]) #Add value to end of other singlet's queue
            else:
                self.duet.qAdd(1-self.id,int(val))
            self.pointer+=1
            if self.id==1:
                self.duet.send1+=1 #Count number of values sent by singlet 1
                print(self.duet.send1)
        elif cat=='rcv': #Receive value instruction
            r=ins.split(' ')[1]
            val=self.duet.qGet(self.id)
            self.reg[r]=int(val)
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
        elif cat=='jgz': #Jump instruction
            val1=ins.split(' ')[1]
            val2=ins.split(' ')[2]
            if val1.isalpha():
                jump=(self.reg[val1]>0)
            else:
                jump=(int(val1)>0)
            if val2.isalpha():
                dist=self.reg[val2]
            else:
                dist=int(val2)
            if jump: #Only jump if val1>0
                self.pointer+=dist
            else:
                self.pointer+=1
        print(self.reg)
                
    def getStatus(self): #Equal to -2 if out of range, else equal to number of stored commands
        #Equal to -1 if no stored commands and next command is rcv
        if (self.pointer<0 or self.pointer>=self.iLen):
            return(-2)
        else:
            qLen=len(self.duet.queue[self.id])
            if (qLen==0 and self.instrs[self.pointer].split(' ')[0]=='rcv'):
                return(-1)
            else:
                return(qLen)
    
def solveB(input):   
    duet=Duet(input)
    sum=None
    while (sum==None):
        sum=duet.runNext()
    return(sum)

retB=solveB(input)