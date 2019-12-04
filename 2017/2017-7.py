# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 21:53:47 2017

@author: Simon
"""

#Advent of Code 2017 Day 7

class NodeList():
    def __init__(self):
        self.nodelist={}
        
    def __iter__(self):
        return(iter(self.nodelist.keys()))
        
    def addNode(self,node):
        if self.nodelist=={}:
            self.firstnode=node #Arbitrary start point
        self.nodelist[node.name]=node
        
    def getNode(self,name):
        return(self.nodelist[name])

class Node():
    def __init__(self,name,weight,children):
        self.name=name
        self.weight=weight
        self.children=children
        self.tweightset=0
        
    def __str__(self):
        res=self.name+' ('+str(self.weight)+') -> '+str(self.children)
        return(res)
        
    def setTotalWeight(self,totweight):
        self.totweight=totweight
        self.tweightset=1 #flag that total weight has been set
        

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-7.txt')
contents = f.read()
file_as_list = contents.splitlines()


def importList(input):
    nList=NodeList()
    for n in input:
        name=n.split()[0]
        weight=int(''.join([s for s in n if s.isdigit()]))
        children=[]
        if '>' in n:
            childstr=n.split('> ')[1]
            children=childstr.split(', ')
        nList.addNode(Node(name,weight,children))
    return(nList)

input=importList(file_as_list)

def solveA(input):
    
    node=input.firstnode
    step=0
    while (step<100000):
        step+=1
        print('Step '+str(step))
        found=0
        for n in input:
            if node.name in input.getNode(n).children:     
                node=input.getNode(n)
                found=1
        if found==0:
            return(node)

retA=solveA(input)
print(retA)

def totalWeight(node): #Find weight of current node and every node above
    total=node.weight
    if node.children!=[]: #Add weight of children if they exist
        for n in node.children:
            child=input.getNode(n)
            total+=totalWeight(child)
    return(total)

def solveB(input):
#    node=solveA(input) #Start at the base node
    node=input.getNode('ihnus')
    step=0
    while (step<1000000):
        step+=1
        weights={}
        wlist=[]
        allequal=1
        for kid in node.children:
            w=totalWeight(input.getNode(kid))
            weights[kid]=w
            wlist.append(w)
        m=max(wlist,key=wlist.count)
        for n in iter(weights.keys()):
            if weights[n]!=m:
                node=input.getNode(n)
                allequal=0
                break
        if allequal==1: #If all weights are equal then we are above the issue
            print('All weights equal for node '+node.name)
            return(node)
            
            
retB=solveB(input)
print(retB)
#ug=input.getNode('ugml')
#wt=totalWeight(ug)
#c=[1,2,2,3,3]
#md=max(c, key = c.count)