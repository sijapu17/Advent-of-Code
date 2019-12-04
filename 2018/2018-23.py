#Advent of Code 2018 Day 23

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-23.txt')
input = f.read().splitlines()
import re
import math
import heapq

class Bot():
    def __init__(self,id,x,y,z,radius):
        self.x, self.y, self.z = x, y, z
        self.id=id
        self.radius = radius
        
    def distFrom(self, other):
        return(abs(self.x-other.x)+abs(self.y-other.y)+abs(self.z-other.z))
    
    def inRange(self,other): #Return true if other bot is within signal radius
        return(self.distFrom(other)<=self.radius)
    
    def __str__(self):
        return(str(self.id)+' <'+','.join([str(self.x),str(self.y),str(self.z)])+'>, r='+str(self.radius))
    
    def __repr__(self):
        return(self.__str__())

class Space():
    def __init__(self,input): #Turn input into points in space
        self.bots={}
        p1=re.compile('pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)')
        i=0
        for p in input:
            m=p1.match(p)
            self.bots[i]=Bot(i,int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)))
            i+=1
        self.minX=min([a.x for a in self.bots.values()])
        self.minY=min([a.y for a in self.bots.values()])
        self.minZ=min([a.z for a in self.bots.values()])
        self.maxX=max([a.x for a in self.bots.values()])
        self.maxY=max([a.y for a in self.bots.values()])
        self.maxZ=max([a.z for a in self.bots.values()])
        
    def getStrongest(self): #Return ID of bot with largest radius
        return(max(self.bots.keys(), key=(lambda k: self.bots[k].radius)))
    
    def nInRange(self,botID): #Return number of bots in range of selected bot
        bot=self.bots[botID]
        count=0
        for b in self.bots.values():
            if bot.inRange(b):
                count+=1
        return(count)
    
    def botIDsInCube(self,botIDs,pos,size): #Return set of IDs of bots in range of the cube
        x0=pos[0]
        y0=pos[1]
        z0=pos[2]
        xSign=math.copysign(1,x0)
        ySign=math.copysign(1,y0)
        zSign=math.copysign(1,z0)
        x1=x0+xSign*size
        y1=y0+ySign*size
        z1=z0+zSign*size
        x=(min(x0,x1),max(x0,x1))
        y=(min(y0,y1),max(y0,y1))
        z=(min(z0,z1),max(z0,z1))
        bots=[self.bots[k] for k in self.bots if k in botIDs]
        inIDs=set()
        for b in bots:
            if x[0]<=b.x<=x[1] and y[0]<=b.y<=y[1] and z[0]<=b.z<=z[1]: #First check if bot is in cube
                inIDs.add(b.id)
            else: #If not in cube, find min dist from point to cube
                distX=max(x[0]-b.x,0,b.x-x[1])
                distY=max(y[0]-b.y,0,b.y-y[1])
                distZ=max(z[0]-b.z,0,b.z-z[1])
                if sum([distX,distY,distZ])<=b.radius: #Check whether min distance is within bot radius
                    inIDs.add(b.id)
        return(inIDs)            

def solveA(input):
    space=Space(input)
    strongest=space.getStrongest()
    return(space.nInRange(strongest))

#retA=solveA(input)
space=Space(input)

class Node(): #Cube within the space to search, counting number of bots in range of any point in the cube
    
    def __init__(self,space,botIDs,size,pos):
        self.space = space
        self.botIDs = botIDs #Only check bots which were in range of the parent node
        self.size = size #Dimension of cube (single point is size 0)
        self.pos = pos #Position of cube corner closest to origin
        self.mDist = sum([abs(d) for d in self.pos]) #Distance from origin
        self.nBots=-1
        #f is heuristic of number of bots in range of node, with ties broken by cube size and mDist from origin
        self.f = (-self.nBots,self.size,self.mDist)

    def __eq__(self, other):
        return (self.size,size.pos) == (other.size,other.pos)
    
    def __lt__(self, other):
        return(self.f<other.f)

    def __gt__(self, other):
        return(self.f>other.f)
    
    def __str__(self):
        return(str(self.pos)+' size='+str(self.size)+' nBots='+str(self.nBots)+' f='+str(self.f))
    
    def __repr__(self):
        return(self.__str__())
    
    def __hash__(self):
        return(hash(str(self.pos)+str(self.size)))

def astar(space):
    """Returns point with most bots in range"""

    longest=0
    
    # Initialize both open heap and closed set
    open_heap = []
    closed_set = set()
    
    # Create 8 start nodes, cutting around origin
    size_needed=max([abs(l) for l in [space.minX,space.maxX,space.minY,space.maxY,space.minZ,space.maxZ]])
    #Find smallest power of 2 that will cover the area
    d=1
    while 2**d<size_needed:
        d+=1
    start_size=2**d
    for i in (0,-1):
        for j in (0,-1):
            for k in (0,-1):                
                node = Node(space=space,botIDs=space.bots,size=start_size,pos=(i,j,k))
                heapq.heappush(open_heap,node)
    
    n=0

    # Loop until you find the end
    while len(open_heap) > 0:
        
        n+=1

        candidate_node = heapq.heappop(open_heap) #Find node in open set with lowest f
        current_node=candidate_node
        #print(str(n)+': Current node '+str(current_node))


        if n%50==1:
            print(str(n)+': Current node '+str(current_node))

        # Found the goal
        if current_node.size == 0:
            print('Pos='+str(current_node.pos)+' mDist='+str(current_node.mDist))
            return(current_node)
        else:
            # Generate children
            children = getChildren(current_node)
            #print('Children '+str(children))
            # Loop through children
            for child in children:
                #print('Child: '+str(child))
                child.botIDs=child.space.botIDsInCube(child.botIDs,child.pos,child.size)
                child.nBots=len(child.botIDs)
                child.f = (-child.nBots,child.size,child.mDist)

                heapq.heappush(open_heap,child)

def getChildren(node): #Produce a list of 8 positions of child subcubes
    x=node.pos[0]
    y=node.pos[1]
    z=node.pos[2]
    out=[]
    newSize=int(node.size/2)
    for i in (0,newSize):
        for j in (0,newSize):
            for k in (0,newSize):
                newPos=(int(x+math.copysign(i,x)),int(y+math.copysign(j,y)),int(z+math.copysign(k,z)))
                out.append(Node(space=node.space,botIDs=node.botIDs,size=newSize,pos=newPos))
    return(out)

retB=astar(space)