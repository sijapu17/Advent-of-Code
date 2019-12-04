#Advent of Code 2016 Day 10

import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-10.txt')
contents = f.read()
input = contents.splitlines()

class Factory():
    def __init__(self):
        self.botlist={}
        self.outputs={} #Outputs and their contents
        
    def __iter__(self):
        return(iter(self.botlist.keys()))
    
    def __str__(self):
        ret=''
        for i in self:
            ret+=str(self.getBot(i))+'\n'
        return(ret)
        
    def addBot(self,bot):
        self.botlist[bot.id]=bot
        
    def getBot(self,id):
        if id not in self.botlist:
            self.addBot(Bot(self,id))
        return(self.botlist[id])
    
    def intoOutput(self,outID,value):
        self.outputs[outID]=int(value)
    
class Bot():
    def __init__(self,factory,id):
        self.factory=factory
        self.id=id
        self.chips=[]
        self.nChips=0
        
    def __str__(self):
        ret='Bot '+str(self.id)+': Chips'+str(self.chips)
        return(ret)
        
    def addChip(self,chip):
        self.chips.append(chip)
        self.nChips+=1
        
    def transfer(self,targets):
        cMin=min(self.chips)
        cMax=max(self.chips)
        #if cMin==17 and cMax==61:
        #    return(self)
        if targets[0]=='bot':
            self.factory.getBot(targets[1]).addChip(cMin)
        elif targets[0]=='output':
            self.factory.intoOutput(targets[1],cMin)
        if targets[2]=='bot':
            self.factory.getBot(targets[3]).addChip(cMax)
        elif targets[2]=='output':
            self.factory.intoOutput(targets[3],cMax)
        self.nChips=0
        self.chips=[]
        
def solveA(input):
    factory=Factory()
    p1=re.compile('^value (\d+) goes to bot (\d+)$')
    p2=re.compile('^bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)$')
    inits=[] #List of initialisation instructions
    passes=[] #List of passing instructions
    for inst in input:
        if p1.match(inst):
            inits.append(inst)
        elif p2.match(inst):
            m2=p2.match(inst)
            passes.append([m2.group(1),m2.group(2),m2.group(3),m2.group(4),m2.group(5)])
    for inst in inits:
        m1=p1.match(inst)
        bot=factory.getBot(m1.group(2)) #Create/fetch bot
        bot.addChip(int(m1.group(1))) #Give chip to bot
        factory.addBot(bot) #Add bot to list
    for each in factory:
        print(factory.getBot(each))
    i=0
    while True and i<5000:
        i+=1
        for p in passes:
            if factory.getBot(p[0]).nChips==2:
                print('Transfer from '+str(bot))
                factory.getBot(p[0]).transfer(p[1:])
    print('------')
    for each in factory:
        print(factory.getBot(each))                
    print('------')
    return(factory)

#input=['value 2 goes to bot 166','value 1 goes to bot 166']
retA=solveA(input)
out=retA.outputs
retB=out['0']*out['1']*out['2']