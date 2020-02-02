#Advent of Code 2019 Day 24 Part 1

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-24.txt')
contents = f.read()
input=contents.splitlines()
import math

class Area():
    def __init__(self,input):
        self.map={}
        j=0
        for row in input:
            i=0
            for g in row:
                pos=complex(i,j)
                self.map[pos]=g
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
                if (i==0 or j==0) and i!=j: #Only count 4 adjacent neighbours
                    nPos=pos+i+j
                    if nPos in self.map.keys():
                        if self.map[nPos]==contents:
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
    
    def bioRating(self): #Defined as the sum of each bug in increasing powers of 2 based on reading order
        count=0
        for j in range(5):
            for i in range(5):
                if self.map[complex(i,j)]=='#':
                    count+=int(math.pow(2,5*j+i))
        return(count)
    
    def update(self): #Check adjacent acres and update each acre
        newItems={}
        for k,v in self.map.items():
            if v=='#':
                if self.nAdjacent(k,'#')==1:
                    newItems[k]='#'
                else:
                    newItems[k]='.'
            elif v=='.':
                if self.nAdjacent(k,'#') in (1,2):
                    newItems[k]='#'
                else:
                    newItems[k]='.'
        for k in newItems.keys():
            self.map[k]=newItems[k]
                
    def __str__(self,letters=False):
        ret1=' '
        ret2=''
        for i in range(self.minX,self.maxX+1):
            ret1+=str(abs(i)%10) #Create units row at top
        for j in range(self.minY,self.maxY+1):

            ret2+=str(abs(j)%10) #Create units column going down
            for i in range(self.minX,self.maxX+1):
                pos=complex(i,j)
                symbol=self.map[pos]
                ret2+=symbol
            ret2+='\n'
        return(ret1+'\n'+ret2)

def keyFromVal(dict,val):
    for k,v in dict.items():
        if val==v:
            return(k)

def solveA(input):
    area=Area(input)
    print(area)
    states={area.bioRating()} #bioRating serves as a unique encoding of state
    for n in range(1000):
        if n%20==1:
            print('n='+str(n))
        area.update()
        rating=area.bioRating()
        if rating in states:
            return(rating)
        states.add(rating)


retA=solveA(input)