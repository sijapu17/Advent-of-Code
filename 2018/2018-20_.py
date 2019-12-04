#Advent of Code 2018 Day 20

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-20.txt')
input = f.read()
from collections import deque

input='^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
input='^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'

class Room():
    def __init__(self,map,pos,minDist):
        self.pos=pos
        self.doors=set()
        self.minDist=minDist
        map[self.pos]=self
        
    def addDoor(self,door):
        self.doors.add(door)
        
    def __str__(self):
        return('Room '+str(self.pos)+' '+str(self.minDist)+' '+str(self.doors))
       
class Node(): #A node has a current position and a regex to explore further
    def __init__(self,pos,regex,dist):
        self.pos=pos
        self.regex=regex
        self.dist=dist
        
    def __str__(self):
        reg=''
        regex=self.regex.copy()
        for n in range(min(len(self.regex),25)):
            reg+=regex.popleft()
        if len(regex)>0:
            reg+='...'
        return('Node '+str(self.pos)+' '+str(self.dist)+' '+reg)

def splitRegex(regex): #Split regex into sections where (|) notation is encountered
    inReg=regex.copy()
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
    #for s in sections:
    #    s+=inReg.copy()
    #ALternatively put remaining regex as a separate node
    sections.append(deque(inReg.copy()))
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
                    
def nodeID(pos,regex,dist): #Create unique ID for a node, made of pos and regex
    return(str(pos)+' '+str(dist)+' '+str(regex))

def makeMap(input):
    map={}
    dirs={'N':complex(0,1),'W':complex(-1,0),'S':complex(0,-1),'E':complex(1,0)}
    opposites={'N':'S','S':'N','W':'E','E':'W'}
    sRoom=Room(map,complex(0,0),0)
    sNode=Node(sRoom.pos,deque(input[1:-1]),0)
    queue=deque([sNode])
    visited=set()
    t=0
    while len(queue)>0:
        #Look at node
        node=queue.popleft()
        visited.add(nodeID(node.pos,node.regex,node.dist))
        if t%100==1:
            print('t='+str(t)+' q='+str(len(queue))+' regex length '+str(len(node.regex)))
        #if node.pos==complex(-1,-2):
        #print(node)
        #Find corresponding room
        room=map[node.pos]
        #print(room) #look at (-3-2j) in 31 example
        #Check whether the node has reached the room in a shorter path then previously
        if node.dist<room.minDist:
            room.minDist=node.dist
        #Look at next direction
        nextDir=node.regex.popleft()
        if nextDir in 'NESW':
            room.addDoor(nextDir)
            nextPos=room.pos+dirs[nextDir]
            nextDist=node.dist+1
            if nextPos in map: #If room already in map
                nextRoom=map[nextPos]
                nextRoom.minDist=min(nextRoom.minDist,nextDist) #Update minDist if shorter route found
            else:
                nextRoom=Room(map,nextPos,nextDist)
                #print('New '+str(nextRoom))
            nextRoom.addDoor(opposites[nextDir]) #Add door that was entered from
            nextRegex=[node.regex.copy()]
        elif nextDir=='(': #Split brackets out into options
            node.regex.appendleft('(')
            nextRegex=splitRegex(node.regex)
        for r in nextRegex:
            if len(r)>0: #If more directions to check, create new node
                if nodeID(nextPos,r,nextDist) not in visited:
                    newNode=Node(nextPos,r,nextDist)
                    queue.append(newNode)
        t+=1
    #Find largest distance
    maxDist=0
    for v in map.values():
        if v.minDist>maxDist:
            maxDist=v.minDist
    print('Longest path is '+str(maxDist))
    return(map)
         
map=makeMap(input)
printMap(map)
#3541 too high