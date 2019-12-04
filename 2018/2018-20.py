#Advent of Code 2018 Day 20

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-20.txt')
input = f.read()
from collections import deque

#23 doors
#input='^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
#31 doors
#input='^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'

class Room():
    def __init__(self,map,pos):
        self.pos=pos
        self.doors=set()
        map[self.pos]=self
        
    def addDoor(self,door):
        self.doors.add(door)
        
    def __str__(self):
        return('Room '+str(self.pos)+' '+str(self.doors))
       
class Node(): #A node has a current position and a regex to explore further
    def __init__(self,pos,regex):
        self.pos=pos
        self.regex=regex
        
    def __str__(self):
        return('Node '+str(self.pos)+' '+strReg(self.regex,25))

def strReg(deque,maxLen=100):
        reg=''
        regex=deque.copy()
        for n in range(min(len(deque),maxLen)):
            reg+=regex.popleft()
        if len(regex)>0:
            reg+='...'
        return(reg)
            
def splitRegex(regex): #Split regex into sections where (|) notation is encountered
    inReg=regex.copy()
    #print('In='+strReg(inReg))
    c=inReg.popleft()
    if c!='(':
        print('First character should be open bracket, not '+c)
    level=1 #Track current level of bracket nesting
    sections=[deque()]
    pointer=0 #Start in first section
    while level>0:
        c=inReg.popleft()
        #print(sections)
        #print(c)
        if c=='(':
            level+=1
        elif c==')':
            level-=1
        if level==1 and c=='|':
            pointer+=1 #Move into second section
            sections.append(deque())
        else:
            sections[pointer].append(c)
    #Remove ending bracket from last section
    sections[-1].pop()
    #Add remaining regex to end of each section
    for s in sections:
        s+=inReg.copy()
    #print('Out='+str([strReg(x) for x in sections]))
    return(sections)

def printMap(map):
    #Find bounds of map
    minX=int(min(map.keys(),key=lambda x:x.real).real)
    maxX=int(max(map.keys(),key=lambda x:x.real).real)
    minY=int(min(map.keys(),key=lambda x:x.imag).imag)
    maxY=int(max(map.keys(),key=lambda x:x.imag).imag)
    width=maxX-minX+1
    height=maxY-minY+1
    pWidth=2*width+1 #Print width needs to include walls/doors
    pHeight=2*height+1 #Print height needs to include walls/doors
    ret='#'*pWidth+'\n'
    for j in reversed(range(minY,maxY+1)):
        ret+='#'
        south='#' #Create south walls/doors as row is created
        for i in range(minX,maxX+1):
            pos=complex(i,j)
            if pos in map:
                room=map[pos]
                if pos==0:
                    ret+='X'
                else:
                    ret+='.'
                if 'E' in room.doors:
                    ret+='|'
                else:
                    ret+='#'
                if 'S' in room.doors:
                    south+='-'
                else:
                    south+='#'
                south+='#'
            else:
                ret+='  '
                south+='  '
        ret+='\n'+south+'\n'
    print(ret)
                    
def nodeID(pos,regex): #Create unique ID for a node, made of pos and regex
    return(str(pos)+' '+str(regex))

def makeMap(input):
    map={}
    dirs={'N':complex(0,1),'W':complex(-1,0),'S':complex(0,-1),'E':complex(1,0)}
    opposites={'N':'S','S':'N','W':'E','E':'W'}
    sRoom=Room(map,complex(0,0))
    sNode=Node(sRoom.pos,deque(input[1:-1]))
    stack=deque([sNode])
    visited=set()
    t=0
    while len(stack)>0:
        #Look at node
        node=stack.popleft()
        visited.add(nodeID(node.pos,node.regex))
        if t%100==1:
            print('t='+str(t)+' q='+str(len(stack))+' regex length '+str(len(node.regex)))
        #if node.pos==complex(-1,-2):
        #print(node)
        #Find corresponding room
        room=map[node.pos]
        #print(room) #look at (-3-2j) in 31 example
        #Look at next direction
        nextDir=node.regex.popleft()
        if nextDir in 'NESW':
            room.addDoor(nextDir)
            nextPos=room.pos+dirs[nextDir]
            if nextPos in map: #If room already in map
                nextRoom=map[nextPos]
            else:
                nextRoom=Room(map,nextPos)
                #print('New '+str(nextRoom))
            nextRoom.addDoor(opposites[nextDir]) #Add door that was entered from
            nextRegex=[node.regex.copy()]
        elif nextDir=='(': #Split brackets out into options
            node.regex.appendleft('(')
            nextRegex=splitRegex(node.regex)
        for r in nextRegex:
            if len(r)>0: #If more directions to check, create new node
                if nodeID(nextPos,r) not in visited:
                    newNode=Node(nextPos,r)
                    stack.appendleft(newNode)
        t+=1
    return(map)
         
map=makeMap(input)
printMap(map)
#3541 too high

class pathNode(): #A path node consists of a room position and the number of doors taken from the start room
    def __init__(self,room,dist):
        self.room=room
        self.pos=room.pos
        self.dist=dist
        
    def __str__(self):
        return(str(self.room)+' '+str(self.dist)+' doors from start')
        
def solveA(map): #Find largest number of doors required to reach a room
    dirs={'N':complex(0,1),'W':complex(-1,0),'S':complex(0,-1),'E':complex(1,0)}
    unvisited=set(map.keys())
    sNode=pathNode(map[0],0) #Starting room
    queue=deque([sNode]) #Queue for BFS
    while len(queue)>0:
        node=queue.popleft()
        #print(node)
        if node.pos in unvisited:
            unvisited.remove(node.pos)
            if len(unvisited)==0:
                return(node.dist)
            #print('node.room.doors='+str(node.room.doors))
            for d in node.room.doors:
                newPos=node.pos+dirs[d]
                #print('newPos='+str(newPos))
                if newPos in unvisited:
                    queue.append(pathNode(map[newPos],node.dist+1))
    
#retA=solveA(map)

def solveB(map): #Find number of rooms with shortest path >=1000
    dirs={'N':complex(0,1),'W':complex(-1,0),'S':complex(0,-1),'E':complex(1,0)}
    unvisited=set(map.keys())
    sNode=pathNode(map[0],0) #Starting room
    queue=deque([sNode]) #Queue for BFS
    while len(queue)>0:
        node=queue.popleft()
        #print(node)
        if node.pos in unvisited:
            if node.dist>=1000:
                return(len(unvisited))
            unvisited.remove(node.pos)
            #if len(unvisited)==0:
            #    return(node.dist)
            #print('node.room.doors='+str(node.room.doors))
            for d in node.room.doors:
                newPos=node.pos+dirs[d]
                #print('newPos='+str(newPos))
                if newPos in unvisited:
                    queue.append(pathNode(map[newPos],node.dist+1))
                    
retB=solveB(map)