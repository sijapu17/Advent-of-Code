#Advent of Code 2018 Day 18

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-18.txt')
contents = f.read()
input=contents.splitlines()
import math

class Forest():
    def __init__(self,input):
        self.map={}
        j=0
        for row in input:
            i=0
            for g in row:
                pos=complex(i,j)
                if g=='.':
                    x='o'
                elif g=='|':
                    x='t'
                elif g=='#':
                    x='l'
                self.map[pos]=x
                i+=1
            j+=1
                
        #Find bounds of map
        self.minX=int(min(self.map.keys(),key=lambda x:x.real).real)
        self.maxX=int(max(self.map.keys(),key=lambda x:x.real).real)
        self.minY=int(min(self.map.keys(),key=lambda x:x.imag).imag)
        self.maxY=int(max(self.map.keys(),key=lambda x:x.imag).imag)
    
    def nAdjacent(self,pos,contents):
        count=0
        for i in (-1,0,1):
            for j in (-1j,0,1j):
                if i!=j: #Do not count acre as its own neighbour
                    nPos=pos+i+j
                    if nPos in self.map.keys():
                        if self.map[nPos].lower()==contents:
                            count+=1
        return(count)
                    
    def nTotal(self,contents):
        count=0
        for k,v in self.map.items():
            if v==contents:
                count+=1
        return(count)
    
    def strMap(self):
        ret=''
        for v in self.map.values():
            ret+=v
        return(ret)
    
    def resourceValue(self): #Defined as number of trees times number of lumberyards
        return(self.nTotal('t')*self.nTotal('l'))
    
    def update(self): #Check adjacent acres and update each acre
        for k,v in self.map.items():
            if v=='o':
                if self.nAdjacent(k,'t')>=3:
                    self.map[k]='O'
            elif v=='t':
                if self.nAdjacent(k,'l')>=3:
                    self.map[k]='T'
            elif v=='l':
                if self.nAdjacent(k,'l')==0 or self.nAdjacent(k,'t')==0:
                    self.map[k]='L'
        #print(self.__str__(letters=True))
        changes={'O':'t','T':'l','L':'o'}
        for k,v in self.map.items():
            if v in changes:
                self.map[k]=changes[v]
                
    def __str__(self,letters=False):
        syms={'o':'.','t':'|','l':'#'}
        ret1='  '
        ret2='  '
        ret3=''
        for i in range(self.minX,self.maxX+1):
            if i%10==0: #Create tens row at top
                ret1+=str(math.floor(abs(i)/10%10))
            else:
                ret1+=' '
            ret2+=str(abs(i)%10) #Create units row at top
        for j in range(self.minY,self.maxY+1):
            if j%10==0:
                ret3+=str(math.floor(abs(j)/10%10)) #Create tens column going down
            else:
                ret3+=' '
            ret3+=str(abs(j)%10) #Create units column going down
            for i in range(self.minX,self.maxX+1):
                pos=complex(i,j)
                if letters:
                    symbol=self.map[pos]
                else:
                    symbol=syms[self.map[pos]]
                ret3+=symbol
            ret3+='\n'
        return(ret1+'\n'+ret2+'\n'+ret3)

def keyFromVal(dict,val):
    for k,v in dict.items():
        if val==v:
            return(k)

def solveA(input):
    forest=Forest(input)
    #print(forest)
    states={}
    for n in range(1000):
        if n%20==1:
            print('n='+str(n))
        forest.update()
        if n>100:
            if n in (451,479):
                print(str(n))
                print(forest)
            val=forest.strMap()
            if val in states.values():
                k=keyFromVal(states,val)
                print(str(n))
                print(str(k))
                period=n-k
                return(period)
            states[n]=val
        #print(forest.resourceValue())
    #return(forest.resourceValue())

#period=solveA(input)

def findStep(total,period,start): #Find first total mod period greater than start
    md=total%period
    while md<start:
        md+=period
    return(md)

step=findStep(1000000000,28,451)

def solveB(input,step):
    forest=Forest(input)
    for n in range(step):
        if n%20==1:
            print('n='+str(n))
        forest.update()
    return(forest.resourceValue())

retB=solveB(input,step)