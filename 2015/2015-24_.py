#Advent of Code 2015 Day 24
import copy
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-24.txt')
contents = f.read()
input = contents.splitlines()

packages=[int(x) for x in input]
packages.reverse()

class Sleigh():
    
    def __init__(self):
        self.packs={}
        self.wght={}
        self.nPack={}
        for i in range(3):
            self.packs[i]=[]
            self.wght[i]=0
            self.nPack[i]=0
        self.maxWght=0
        
    def __str__(self):
        res=str(self.packs)+' '+str(self.wght)
        return(res)
            
    def addPack(self,wght,cpt):
        new=copy.deepcopy(self)
        new.packs[cpt].append(wght)
        new.wght[cpt]+=wght
        new.nPack[cpt]+=1
        new.maxWght=max(new.wght.values())
        return(new)
        
def solveA(input):
    
    cptWght=int(sum(packages)/3) #Weight required for each compartment
    print(str(cptWght)+' per compartment')
    
    sleigh=Sleigh()
    sleighs=[sleigh.addPack(input[0],0)] #Always put first package in first compartment to reduce duplication
    
    for i in range(1,len(input)):
        print('Package '+str(i))
        l=len(sleighs)
        print(str(l)+' sleighs')
        new=[]
        for j in range(l):
            oldSleigh=sleighs[j]
            for k in range(3):
                newSleigh=oldSleigh.addPack(input[i],k)
                if newSleigh.maxWght<=cptWght:
                    new.append(newSleigh)
        sleighs=copy.deepcopy(new)
    
    return(sleighs)

retA=solveA(packages)