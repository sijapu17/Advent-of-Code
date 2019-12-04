#Advent of Code 2016 Day 17

import hashlib
input='pvhmgsws'

def mHash(instr): #Calculate first 4 chars of MD5 hash
    m=hashlib.md5(instr.encode()).hexdigest()
    return(m[:4])

def openDoors(hStr): #Find which doors are open
    dirs={0:'U', 1:'D', 2:'L', 3:'R'}
    ret=''
    for i in range(4):
        if hStr[i] in 'bcdef':
            ret+=dirs[i]
    return(ret)

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self,input,pos=None,path=''):
        self.input = input
        self.pos = pos
        self.path = path

        self.g = 0
        self.h = h(pos)
        self.f = 0

    def __eq__(self, other):
        return self.path == other.path
    
    def __str__(self):
        h=mHash(self.input+self.path)
        dirs=openDoors(h) #Determine open doors from current path
        return(str(self.pos)+' '+str(self.path)+' g='+str(self.g)+' h='+str(self.h)+' f='+str(self.f)+' next='+str(dirs))
    
    def __hash__(self):
        return(hash(str(self.path)))

def astar(input):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    longest=0
    # Create start and end node
    start_node = Node(input=input,pos=0+0j)

    # Initialize both open and closed list
    open_list = []
    #closed_list = set()

    # Add the start node
    open_list.append(start_node)
    
    n=0

    # Loop until you find the end
    while len(open_list) > 0:
        
        n+=1

        #current_node = open_list[0]

        #current_index = 0
        #for index, item in enumerate(open_list):
        #    if item.f < current_node.f:
        #        current_node = item
        #        current_index = index

        # Pop current off open list, add to closed list
        current_node = open_list.pop()
        #closed_list.add(current_node)

        #if n%50==1:
        #print(str(n)+': Current node '+str(current_node))

        # Found the goal
        if h(current_node.pos) == 0:
            print('Steps='+str(current_node.g)+' Path='+str(current_node.path))
            longest=max(longest,current_node.g)
        else:
            # Generate children
            children = getChildren(input,current_node)
            #print('Children '+str(children))
            # Loop through children
            for child in children:

                # Child is on the closed list
                #seen=False
                #for closed_child in closed_list:
                #    if child.path == closed_child.path:
                #        seen=True

                #if not seen:
                    # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = h(child.pos)
                child.f = child.g + child.h

                # Child is already in the open list
                #inOpen=False
                #for open_node in open_list:
                #    if child.path == open_node.path and child.g >= open_node.g:
                #        inOpen=True

                #if not inOpen:
                    # Add the child to the open list
                open_list.append(child)
                
            #open_list=[x for x in open_list if x not in closed_list]
        
    return(longest)

def h(pos): #Calculate h-value of pos (i.e. minimum number of steps from current state to end)
    out=min(1,abs(3-pos.real)+abs(-3-pos.imag))
    return(out)

def getChildren(input,node): #Produce a list of all possible children (next steps) of node
    pos=node.pos
    h=mHash(input+node.path)
    dirs=openDoors(h) #Determine open doors from current path
    out=[]
    jDirs={'U':1j, 'D':-1j, 'L':-1, 'R':1}
    for d in dirs:
        new=pos+jDirs[d]
        if new.real in [0,1,2,3] and new.imag in [0,-1,-2,-3]: #Pos must be in 4x4 grid
            out.append(Node(input=input,pos=new,path=node.path+d))
    return(out)

#input='hijkl' #Test input
retA=astar(input)