#Advent of Code 2017 Day 13

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-13.txt')
contents = f.read()
file_as_list = contents.splitlines()

class Firewall():
    def __init__(self):
        self.layerList={}
        
    def __iter__(self):
        return(iter(self.layerList.values()))
        
    def addLayer(self,layer):
        if self.layerList=={}:
            self.maxDepth=layer.depth #Max layer in firewall
        else:
            self.maxDepth=max(self.maxDepth,layer.depth)
        self.layerList[str(layer.depth)]=layer
        
    def getLayer(self,depth):
        return(self.layerList[depth])

class Layer():
    def __init__(self,depth,Range):
        self.depth=depth
        self.Range=Range
        if range==1:
            self.stateList=[0]
        else:
            self.stateList=list(range(self.Range))[:self.Range-1:1]+list(range(self.Range))[:0:-1]
        
    def __str__(self):
        res=self.depth+str(self.range)
        return(res)
    
    def scanPos(self,step):
        return(self.stateList[step%len(self.stateList)])
            
def importFirewall(input):
    fWall=Firewall()
    for n in input:
        depth=int(n.split(': ')[0])
        Range=int(n.split(': ')[1])
        fWall.addLayer(Layer(depth,Range))
    return(fWall)

input=importFirewall(file_as_list)
#inputex=importFirewall(['0: 3','1: 2','4: 4','6: 4'])
                     
def tripSeverity(input,delay=0): #Find severity of trip through firewall
    severity=0
    for l in input:
        scanpos=l.scanPos(l.depth+delay)
        if scanpos==0:
            severity+=l.depth*l.Range
            print('Caught at depth '+str(l.depth)+' range '+str(l.Range))
        else:
            print('Escaped at depth '+str(l.depth)+' range '+str(l.Range)+' scanPos='+str(scanpos))
    return(severity)

def Caught(input,delay=0): #Find severity of trip through firewall
    for l in input:
        scanpos=l.scanPos(l.depth+delay)
        if scanpos==0:
            #print('Caught at depth '+str(l.depth)+' range '+str(l.Range))
            return('Caught')

#one=inputex.getLayer('1')
#retA=tripSeverity(input)

def findDelay(input): #Find delay which allows packet to pass undetected
    delay=0
    while (delay<=24504480):
        if delay%50==0:
            print('Delay='+str(delay))
        status=Caught(input,delay)
        if (status!='Caught'):
            return(delay)
        delay+=1
        
def ranges(input):
    rngs=[]
    for i in input:
        rngs.append(2*(i.Range-1))
    return(rngs)

#vals=ranges(input)

#from fractions import gcd
#lcm = vals[0]
#for i in vals[1:]:
#  lcm = lcm*i/gcd(lcm, i)
#print(lcm)

retB=findDelay(input)
        