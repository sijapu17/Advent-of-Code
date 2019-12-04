#Advent of Code 2016 Day 22

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-22.txt')
input = f.read().splitlines()
import re
import math

class Node():
    def __init__(self,pos,size,used,avail,pct):
        self.pos,self.size,self.used,self.avail,self.pct=pos,size,used,avail,pct
        if self.used==0:
            self.status='_'
        elif self.used<100:
            self.status='.'
        else:
            self.status='#'

def parse(input):
    cluster={}
    p1=re.compile('\/dev\/grid\/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')
    for i in input[2:]:
        m=p1.match(i)
        pos=complex(int(m.group(1)),int(m.group(2)))
        cluster[pos]=Node(pos,int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6)))
    return(cluster)

cluster=parse(input)
        
def solveA(cluster):
    count=0
    for n in cluster.values():
        if n.used>0:
            count+=len([x for x in cluster.values() if x.pos!=n.pos and x.avail>=n.used])
    return(count)

#retA=solveA(cluster)

def printmap(cluster):
    minX=int(min(cluster.keys(),key=lambda x:x.real).real)
    maxX=int(max(cluster.keys(),key=lambda x:x.real).real)
    minY=int(min(cluster.keys(),key=lambda x:x.imag).imag)
    maxY=int(max(cluster.keys(),key=lambda x:x.imag).imag)
    ret1='  '
    ret2='  '
    ret3=''
    for i in range(minX,maxX+1):
        if i%10==0: #Create tens row at top
            ret1+=str(math.floor(abs(i)/10%10))
        else:
            ret1+=' '
        ret2+=str(abs(i)%10) #Create units row at top
    for j in range(minY,maxY+1):
        if j%10==0:
            ret3+=str(math.floor(abs(j)/10%10)) #Create tens column going down
        else:
            ret3+=' '
        ret3+=str(abs(j)%10) #Create units column going down
        for i in range(minX,maxX+1):
            pos=complex(i,j)
            ret3+=cluster[pos].status
        ret3+='\n'
    print(ret1+'\n'+ret2+'\n'+ret3)

printmap(cluster)
