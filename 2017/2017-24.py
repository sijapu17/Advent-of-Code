#Advent of Code 2017 Day 24

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2017-24.txt')
contents = f.read()
file_as_list = contents.splitlines()

class PartList(): #List of parts
    def __init__(self):
        self.partlist={}
        self.usedID=[] #List of IDs of used parts
        self.weight=0
        self.endPort=0 #Size of current end port
        
    def __iter__(self):
        return(iter(self.partlist.keys()))
    
    def pCopy(self): #create unlinked copy of self
        ret=PartList()
        ret.partlist=self.partlist
        ret.usedID=self.usedID.copy()
        ret.weight=self.weight
        ret.endPort=self.endPort
        return(ret)
        
    def addPart(self,part):
        self.partlist[part.id]=part
        
    def getPart(self,id):
        return(self.partlist[id])
    
    def addUsed(self,id):
        self.usedID.append(id)
        
    def __str__(self): #Print current bridge
        res=''
        for i in self.usedID:
            res+=str(self.partlist[i].ports)
            res+=','
        return(res[:-1])

class Part():
    def __init__(self,id,ports):
        self.id=id
        portsS=ports.split('/')
        self.ports=[int(x) for x in portsS]
        self.weight=sum(self.ports)
        
        
    def __str__(self):
        res=str(self.id)+str(self.ports)
        return(res)


def importList(input):
    pList=PartList()
    i=1
    for n in input:
        pList.addPart(Part(i,n))
        i+=1
    return(pList)

input=importList(file_as_list)

def DFS(input): #Find max bridge weight
    stack=[input.pCopy()]
    mxWt=0
    while len(stack)>0:
        #print([str(x) for x in stack])
        bridge=stack.pop() #Take last bridge from stack
        ePort=bridge.endPort #Save current endport for comparison
        #print(bridge)
        for pt in bridge.partlist: #Check through partlist for suitable next part
            #print('ID'+str(pt))
            part=bridge.partlist[pt]
            if part.id not in bridge.usedID: #Cannot use a part twice
                if part.ports[0]==ePort or part.ports[1]==ePort: #Part must fit end of bridge
                    bridge1=bridge.pCopy()
                    bridge1.weight+=part.weight
                    if bridge1.weight>mxWt: #Update if max weight found
                        mxWt=bridge1.weight
                    bridge1.addUsed(part.id)
                    #print('Wt '+str(bridge1.weight))
                    #print('IDs '+str(bridge1.usedID))
                    if part.ports[0]==ePort:
                        bridge1.endPort=part.ports[1]
                    else:
                        bridge1.endPort=part.ports[0]
                    #print(bridge1.endPort)
                    stack.append(bridge1)
            #print([str(x) for x in stack])
    return(mxWt)
                
retA=DFS(input)
                
                