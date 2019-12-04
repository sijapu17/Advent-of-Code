#Advent of Code 2018 Day 22

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-22.txt')
input = f.read()
import heapq

depth=7740
target=(12,763)

#Example
#depth=510
#target=(10,10)

class Region():
    def __init__(self,pos):
        self.pos=pos
        self.el=None
        self.type=None
        
    def __str__(self):
        return(str(self.pos)+' EL: '+str(self.el)+' '+str(self.type))
        
class Cave():
    def __init__(self,depth,target,border=10):
        self.map={}
        self.target=target
        self.tPos=complex(target[0],target[1])
        for j in range(target[1]+border+1):
            for i in range(target[0]+border+1):
                pos=complex(i,j)
                region=Region(pos)
                self.map[pos]=region
                if i==0:
                    gi=j*48271
                elif j==0:
                    gi=i*16807
                elif (i,j)==target:
                    gi=0
                else:
                    gi=self.map[complex(i-1,j)].el*self.map[complex(i,j-1)].el
                region.el=(gi+depth)%20183
                emod3=region.el%3
                if emod3==0:
                    region.type='.' #rockey
                elif emod3==1:
                    region.type='=' #wet
                elif emod3==2:
                    region.type='|' #narrow
                    
    def __str__(self):
        ret=''
        for j in range(target[1]+1):
            for i in range(target[0]+1):
                ret+=self.map[complex(i,j)].type
            ret+='\n'
        return(ret)
                    
cave=Cave(depth,target)

def riskLevel(cave):
    sum=0
    risk={'.':0,'=':1,'|':2}
    for r in cave.map.values():
        #print(r)
        sum+=risk[r.type]
    return(sum)

#risk=riskLevel(cave) #9948 too high

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self,cave,status=None,path=''):
        self.cave = cave
        self.status = status
        self.path=path

        self.g = 0
        self.h = h(status,self.cave.tPos)
        self.f = self.g+self.h

    def __eq__(self, other):
        return self.status == other.status
    
    def __lt__(self, other):
        return(self.f<other.f)
    
    def __str__(self):
        return(str(self.status)+' g='+str(self.g)+' h='+str(self.h)+' f='+str(self.f))
    
    def __hash__(self):
        return(hash(str(self.status)))

def astar(cave):
    """Returns shortest time from start to target"""

    longest=0
    # Create start and end node
    start_node = Node(cave=cave,status=(complex(0,0),'torch'),path='')

    # Initialize both open and closed set
    open_heap = []
    closed_set = set()

    # Add the start node
    heapq.heappush(open_heap,start_node)
    
    n=0

    # Loop until you find the end
    while len(open_heap) > 0:
        
        n+=1

        candidate_node = heapq.heappop(open_heap) #Find node in open set with lowest f
        if candidate_node in closed_set:
            continue
        current_node=candidate_node
        #print(str(n)+': Current node '+str(current_node))

        #Add current node to closed set
        closed_set.add(current_node)

        if n%50==1:
            print(str(n)+': Current node '+str(current_node))

        # Found the goal
        if h(current_node.status,current_node.cave.tPos) == 0:
            print('Path='+str(current_node.path)+' Minutes='+str(current_node.g))
            return(current_node.g)
        else:
            # Generate children
            children = getChildren(cave,current_node)
            #print('Children '+str(children))
            # Loop through children
            for childPack in children:
                
                child=childPack[0]
                childTime=childPack[1]

                if child not in closed_set:
                    # Create the f, g, and h values
                    child.g = current_node.g + childTime
                    child.h = h(child.status,child.cave.tPos)
                    child.f = child.g + child.h

                    heapq.heappush(open_heap,child)
            
            #Remove any nodes in closed set from open set
            #open_heap = open_heap - closed_set


def h(status,tPos): #Calculate h-value of status (i.e. minimum number of minutes from current state to end)
    pos=status[0]
    tool=status[1]
    out=abs(tPos.real-pos.real)+abs(tPos.imag-pos.imag)
    if tool!='torch': #Must end with torch equipped
        out+=7
    return(out)

def getChildren(cave,node): #Produce a list of all possible children (next steps) of node
    pos=node.status[0]
    tool=node.status[1]
    region=cave.map[pos]
    path=node.path

    out=[]
    dirs={'D':1j, 'U':-1j, 'L':-1, 'R':1}
    allowed={'.':['rope','torch'], '=':['rope','neither'], '|':['torch','neither']}
    for k,v in dirs.items(): #Try moving in four directions
        newPos=pos+v
        if newPos in cave.map: #Pos must be non-negative in both dimensions
            newRegion=cave.map[newPos]
            if tool in allowed[newRegion.type]:
                out.append([Node(cave=cave,status=(newPos,tool),path=path+k),1])
    #Try changing tool
    newTool=next(x for x in allowed[region.type] if x!=tool) #Find other allowed tool for current region
    out.append([Node(cave=cave,status=(pos,newTool),path=path+'X'),7])
    return(out)

retB=astar(cave)

def countTime(path):
    count=0
    for s in path:
        if s=='X':
            count+=7
        else:
            count+=1
    return(count)

time=countTime('DRXDRRXRRRRRRURRDRRURRRUXRDDDDDLLDDLDDDLLDXLLU')