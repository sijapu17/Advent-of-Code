#Advent of Code 2019 Day 18

from collections import deque, defaultdict
import string
import heapq

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-18.txt')
contents = f.read()
input=contents.splitlines()

class Maze(): #Overall class for maze containing map, keys and doors
    
    def __init__(self,input): #Convert input into map and units
        self.map={}
        self.paths=defaultdict(dict)
        self.w=len(input[0])
        self.h=len(input)
        lCase='@'+string.ascii_lowercase #List for keys
        uCase=string.ascii_uppercase #List for doors
        self.keyPositions={}
        self.doorPositions={}
        self.keyNames=set()
        self.doorNames=set()
        self.shortestBetweenKeys=float('Inf')
    
        for j in range(self.h):
            for i in range(self.w):
                x=input[j][i]
                pos=complex(i,j)
                if x in lCase: #Add entries to lookup key from position, or position from key
                    self.keyNames.add(x)
                    self.keyPositions[x]=pos
                elif x in uCase: #Add entries to lookup door from position, or position from door
                    self.doorNames.add(x)
                    self.doorPositions[x]=pos
                self.map[pos]=x
                
        self.nKeys=len(self.keyNames)
        self.findDistances()
                
    def findDistances(self): #Run BFS search to find min distances and doors to get to/from each key
        starts=''.join(sorted(self.keyNames)) #List of starting points of each leg, consisting of the entrance '@' and each key
        for s in starts:
            print(s)
            ends=set(starts[starts.index(s)+1:]) #Paths are reversible so we only need to check ends that are after start in the list
            queue=deque() #BFS queue
            queue.appendleft(BFSNode(self.keyPositions[s],0,set(),set()))
            visited=set() #Track set of visited points, to avoid backtracking
            while len(queue)>0 and len(ends)>0:
                current=queue.pop()
                pos=current.pos
                visited.add(pos)
                tile=self.map[pos]
                if tile in self.doorNames: #If current position is a door, add it to node
                    current.addDoor(tile)
                elif tile in ends: #If current position is a key endpoint, create a path object and add to paths dict
                    path=Path(s,tile,current.dist,current.doors.copy(),current.keys.copy())
                    self.paths[s][tile]=path
                    self.paths[tile][s]=path
                    if current.dist<self.shortestBetweenKeys: #To be used by A* search later
                        self.shortestBetweenKeys=current.dist
                if tile in self.keyNames and tile!=s: #If current position is a key, add it to node
                    current.addKey(tile)                    
                for step in (complex(0,1),complex(0,-1),complex(1,0),complex(-1,0)):
                    if self.map[pos+step]!='#' and pos+step not in visited:
                        queue.appendleft(BFSNode(pos+step,current.dist+1,current.doors.copy(),current.keys.copy()))
                        
    def astar(self): #A* search to find shortest path for collecting all keys
        
        openHeap=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
        closedSet=set() #Set of already-visited states (current position plus set of collected keys)
        
        node=AStarNode(self,0,'@',set('@'),'@') #Start node at entrance '@'
        heapq.heappush(openHeap,node)
        n=0
        while len(openHeap)>0:# and n<1000:
            node=heapq.heappop(openHeap) #Examine node in open heap with lowest f
            if node.__hash__() in closedSet:
                continue #If state has been seen before, skip
            closedSet.add(node.__hash__())
            n+=1
            if n%1000==1:
                print(str(n)+': Current node '+str(node))
            if node.h==0: #Check if current node is solution
                print(str(n)+': Solution node '+str(node))
                return(node)
            #Otherwise expand node
            remainingKeys=self.keyNames-node.found
            for dest in remainingKeys: #For each unvisited key, check whether the path is blocked by any locked doors
                path=self.paths[node.key][dest]
                valid=True #Tracker for valid path (path with no locked doors or uncollected keys in the way
                for door in path.doors:
                    if door.lower() not in node.found: #If a locked door is found, set valid to False and stop checking
                        valid=False
                        break
                if valid:
                    for key in path.keys:
                        if key not in node.found: #If an uncollected key is found in the middle of the path, set valid to False and stop checking
                            valid=False
                            break
                    if valid: #If path is valid, create child node
                        childFound=node.found.copy()
                        childFound.add(dest)
                        childPath=node.path+dest
                        child=AStarNode(self,node.g+path.dist,dest,childFound,childPath)
                        if child.__hash__() not in closedSet:
                            heapq.heappush(openHeap,child)
                            
                            
        print('Nodes exhausted, no solution found')
                    
                   
class Path(): #Path between two keys (or '@' to a key)
    def __init__(self,start,end,dist,doors,keys):
        self.start=start
        self.end=end
        self.dist=dist
        self.doors=doors
        self.keys=keys 
        
    def __repr__(self):
        return(str(self.start)+' to '+str(self.end)+' dist='+str(self.dist)+' Doors: '+str(self.doors)+ ' Keys: '+str(self.keys))

class BFSNode(): #Node for BFS
    def __init__(self,pos,dist,doors,keys):
        self.pos=pos
        self.dist=dist
        self.doors=doors
        self.keys=keys
        
    def addDoor(self,door): #Add door to set of doors visited by node
        self.doors.add(door)
        
    def addKey(self,key): #Add key to set of keys visited by node
        self.keys.add(key)
        
class AStarNode(): #Node for A*
    
    def __init__(self,maze,dist,key,found,path):

        self.maze = maze
        self.key = key #Current key
        self.found=found #Set of all keys found so far
        self.path=path #String path of keys found so far

        self.g = dist #Distance travelled by bot so far
        self.h = self.nodeH()
        self.f = self.g+self.h
        
        self.status=(self.key,self.found) #Node status
        
    def nodeH(self): #Heuristic consisting of the minimum possible distance to end - minimum key-to-key distance in maze multiplied by number of keys left to find
        nLeft=len(self.maze.keyNames)-len(self.found)
        return(nLeft*self.maze.shortestBetweenKeys)

    def __eq__(self, other):
        return self.status == other.status
    
    def __lt__(self, other):
        return(self.f<other.f)
    
    def __str__(self):
        return(str(self.path)+' g='+str(self.g)+' h='+str(self.h)+' f='+str(self.f))
    
    def __hash__(self):
        return(hash(str(self.status)))
        
def solveA(input):
    maze=Maze(input)
    return(maze.astar())

retA=solveA(input)
