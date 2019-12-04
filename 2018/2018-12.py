#Advent of Code 2018 Day 12
from collections import defaultdict
import math
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-12.txt')
contents = f.read()
input=contents.splitlines()

initial=input[0].split()[-1]
noteStr=input[2:]
notes={}

def empty(): #Dummy function to return an empty pot when required
    return('.')

plants=defaultdict(empty)
for n in noteStr:
    nSplit=n.split(' => ')
    notes[nSplit[0]]=nSplit[1]
    
for i in range(len(initial)):
    if initial[i]=='#':
        plants[i]=initial[i]
    
def showPlants(plants):
    mn=min(plants.keys())
    mx=max(plants.keys())
    ret1=''
    ret2=''
    ret3=''
    for i in range(mn,mx+1):
        if i%10==0:
            ret1+=str(math.floor(abs(i)/10%10))
        else:
            ret1+=' '
        ret2+=str(abs(i)%10)
        ret3+=plants[i]
    print(ret1+'\n'+ret2+'\n'+ret3)
    
    
def update(plants,notes): #Update dict of plants for new generation
    mn=min(plants.keys())
    mx=max(plants.keys())
    newPlants=defaultdict(empty)
    for i in range(mn-2,mx+3): #Look at a range up to 2 either side of furthest plants
        region=''
        for j in range(i-2,i+3):
            region+=plants[j]
        if notes[region]=='#':
            newPlants[i]=notes[region]
    return(newPlants)

def solveA(plants,notes,n):
    nPlants=0
    for i in range(500):
        plants=update(plants,notes)
        oldnPlants=nPlants
        nPlants=sum(plants.keys())
        additional=nPlants-oldnPlants
        print('Update '+str(i)+': '+str(additional)+' additional plants')
    ret=nPlants+(50000000000-500)*additional #Additional per update becomes stable
    return(ret)
#50000000000
#retA=solveA(plants,notes,20)
retB=solveA(plants,notes,50000000000)
        