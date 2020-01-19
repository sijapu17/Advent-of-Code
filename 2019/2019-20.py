#Advent of Code 2019 Day 20

from collections import deque, defaultdict
import string
import heapq

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-20.txt')
contents = f.read()
input=contents.splitlines()

class Maze(): #Overall class for maze containing map, keys and doors
    
    def __init__(self,input): #Convert input into map and units
        self.map={}
        self.paths=defaultdict(dict)
        self.w=len(input[0])
        self.h=len(input)
        self.portalNames=set()
        self.innerPortals={}
        self.outerPortals={}
        
        dirs=(complex(0,1),complex(1,0),complex(0,-1),complex(-1,0))
    
        for j in range(self.h):
            for i in range(self.w):
                x=input[j][i]
                pos=complex(i,j)
                if x in ('.','#'): #Add path tile or wall tile to map
                    self.map[pos]=x
                if x=='.': #Check whether path has adjacent portal 
                    for d in dirs:
                        adj=pos+d
                        if input[int(adj.imag)][int(adj.real)] in string.ascii_uppercase:
                            adj2=adj+d #Step once more in same direction to get second character of label
                            self.map[adj]='#' #Add wall to outside of portal to avoid pathing out of the maze
                            if d in (complex(0,1),complex(1,0)): #Down or left
                                label=input[int(adj.imag)][int(adj.real)]+input[int(adj2.imag)][int(adj2.real)]
                            else: #Up or right
                                label=input[int(adj2.imag)][int(adj2.real)]+input[int(adj.imag)][int(adj.real)]
                            #Check whether portal is inner or outer
                            if min(pos.real,pos.imag)<=3 or max(pos.real,pos.imag)>=min(self.h,self.w)-3:
                                pDict=self.outerPortals
                            else:
                                pDict=self.innerPortals
                                label=label.lower() #lowercase indicates inner portal
                            #Map portal position to label
                            pDict[pos]=label
                            pDict[label]=pos
                            self.portalNames.add(label.upper()) #Only store each portal pair once, in uppercase
                            break
                        
        self.portals={**self.innerPortals,**self.outerPortals} #Combine inner and outer portal dictionaries
        self.findDistances()

                
    def findDistances(self): #Run BFS search to find min distances between each portal
        starts=[x for x in self.innerPortals if type(x)==str]+[x for x in self.outerPortals if type(x)==str] #List of portals
        for s in starts:
            ends=set(starts) #From each portal, find closest portal in pair
            ends.remove('AA') #No need to path to start
            ends.discard(s) #Do not path to self
            queue=deque() #BFS queue
            queue.appendleft(BFSNode(self.portals[s],0)) #Add start portal node
            visited=set() #Track set of visited tiles, to avoid backtracking
            while len(queue)>0 and len(ends)>0:
                current=queue.pop()
                pos=current.pos
                visited.add(pos)
                if pos in self.portals: #If current position is a valid portal, create a path object and add to paths dict
                    portal=self.portals[pos]
                if portal in ends:
                    path=Path(s,portal,current.dist)
                    self.paths[s][portal]=path
                    ends.remove(portal) #Remove portal and its counterpart
                    if portal.isupper():
                        ends.discard(portal.lower())
                    else:
                        ends.discard(portal.upper())
                for step in (complex(0,1),complex(0,-1),complex(1,0),complex(-1,0)):
                    if self.map[pos+step]!='#' and pos+step not in visited:
                        queue.appendleft(BFSNode(pos+step,current.dist+1))
        print('Route lengths calculated')
                        
    def astar(self): #A* search to find shortest path for collecting all keys
        
        openHeap=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
        closedSet=set() #Set of already-visited states (current position plus set of collected keys)
        
        node=AStarNode(self,'AA',0,['AA']) #Start node at entrance 'AA'
        heapq.heappush(openHeap,node)
        n=0
        while len(openHeap)>0 and n<10000:
            node=heapq.heappop(openHeap) #Examine node in open heap with lowest f
            if node.__hash__() in closedSet:
                continue #If state has been seen before, skip
            closedSet.add(node.__hash__())
            n+=1
            if n%100==1:
                print(str(n)+': Current node '+str(node))
            if node.current=='END': #Check if current node is solution
                print(str(n)+': Solution node '+str(node))
                return(node)
            #Otherwise expand node
            start=node.current
            for dest in self.paths[start]: #Loop through all possible portals that can be reached from current portal
                if dest in node.path:
                    continue #Do not go through a portal more than once
                path=self.paths[start][dest]
                if dest=='ZZ':
                    childDest='END'
                    childDist=node.dist+path.dist
                else:
                    childDist=node.dist+path.dist+1 #Add 1 to account for jumping through portal
                    if dest.isupper(): #Jump through portal
                        childDest=dest.lower()
                    else:
                        childDest=dest.upper()
                childPath=node.path.copy()
                childPath.append(dest)
                child=AStarNode(self,childDest,childDist,childPath) 
                if child.__hash__() not in closedSet:
                    heapq.heappush(openHeap,child)
                            
                            
        print('Nodes exhausted, no solution found')
                    
                   
class Path(): #Path between two portals
    def __init__(self,start,end,dist):
        self.start=start
        self.end=end
        self.dist=dist
        
    def __repr__(self):
        return(str(self.start)+' to '+str(self.end)+' dist='+str(self.dist))

class BFSNode(): #Node for BFS
    def __init__(self,pos,dist):
        self.pos=pos
        self.dist=dist
        
class AStarNode(): #Node for A*
    
    def __init__(self,maze,current,dist,path):

        self.maze = maze
        self.current=current #Current portal
        self.path=path #List path of portals entered
        self.dist = dist #Distance travelled so far
        
    def __eq__(self, other):
        return self.path == other.path
    
    def __lt__(self, other):
        return(self.dist<other.dist)
    
    def __str__(self):
        return(str(self.path)+' dist='+str(self.dist))
    
    def __hash__(self):
        return(hash(str(self.path)))
        
def solveA(input):
    maze=Maze(input)
    return(maze.astar())

retA=solveA(input)
#maze=Maze(input)