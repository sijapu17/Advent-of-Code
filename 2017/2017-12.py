#Advent of Code 2017 Day 12

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
    def __init__(self,name,nebrs):
        self.name=name
        self.nebrs=nebrs
        
    def __str__(self):
        res=self.name+str(self.nebrs)
        return(res)

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-12.txt')
contents = f.read()
file_as_list = contents.splitlines()

def importList(input):
    nList=NodeList()
    for n in input:
        name=n.split(' <-> ')[0]
        nebrs=[]
        if '>' in n:
            nbstr=n.split(' <-> ')[1]
            nebrs=nbstr.split(', ')
        nList.addNode(Node(name,nebrs))
    return(nList)

input=importList(file_as_list)

n=input.getNode('1')
nm=n.name
nn=n.nebrs

def group0(input): #Find size of group connected to node 0
    visited=[] #List of visited nodes
    toVisit=['0'] #List of nodes to be visited
    while len(toVisit)>0:
        nodestr=toVisit.pop()
        node=input.getNode(nodestr)
        visited.append(nodestr)
        for n in node.nebrs: #Add unvisited neighbours into stack to check
            if (n not in visited):
                toVisit.append(n)
    return(len(visited))

retA=group0(input)

def groupN(input,n,ungrouped): #Find size of group connected to node n
    visited=[] #List of visited nodes
    toVisit=[n] #List of nodes to be visited
    while len(toVisit)>0:
        nodestr=toVisit.pop()
        node=input.getNode(nodestr)
        visited.append(nodestr)
        for n in node.nebrs: #Add unvisited neighbours into stack to check
            if (n not in visited):
                toVisit.append(n)
    for i in visited: #Remove visited nodes from the ungrouped list
        if i in ungrouped:
            ungrouped.remove(i)
    print('Group '+str(n)+': '+str(len(visited))+' items')
    return(ungrouped)

def countGroups(input):
    ungrouped=[]
    count=0
    for nd in input: #Add every node to ungrouped list
        ungrouped.append(nd)
    while len(ungrouped)>0:
        node=ungrouped[0] #Pick first remaining ungrouped node to check
        ungrouped=groupN(input,node,ungrouped)
        count+=1
    return(count)

retB=countGroups(input)