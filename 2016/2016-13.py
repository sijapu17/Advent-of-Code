#Advent of Code 2016 Day 13
import string
import copy
from itertools import combinations
input = 1+1j
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self,parent=None,pos=None,path=[]):
        self.pos = pos
        self.parent = parent
        self.path = path

        self.g = 0
        self.h = h(pos)
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos
    
    def __str__(self):
        return(str(self.pos)+' g='+str(self.g)+' h='+str(self.h)+' f='+str(self.f))
    
    def __hash__(self):
        return(hash((str(self.pos),self.g)))

def astar(input):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(pos=input)
    start_node.g = start_node.h = start_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()

    # Add the start node
    open_list.append(start_node)
    
    n=0

    # Loop until you find the end
    while len(open_list) > 0:
        
        n+=1

        current_node = open_list[0]

        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.add(current_node)

        #if n%50==1:
        print(str(n)+': Current node '+str(current_node))
        # Found the goal
        if h(current_node.pos) == 0:
            print('Steps='+str(current_node.g))
            return(current_node)

        # Generate children
        children = getChildren(current_node)
        #print('Children '+str(children))
        # Loop through children
        for child in children:

            # Child is on the closed list
            seen=False
            for closed_child in closed_list:
                if child.pos == closed_child.pos:
                    seen=True

            if not seen:
                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = h(child.pos)
                child.f = child.g + child.h

                # Child is already in the open list
                inOpen=False
                for open_node in open_list:
                    if child.pos == open_node.pos and child.g >= open_node.g:
                        inOpen=True

                if not inOpen:
                    # Add the child to the open list
                    open_list.append(child)
            
        open_list=[x for x in open_list if x not in closed_list]

def h(pos): #Calculate h-value of pos (i.e. minimum number of steps from current state to end)
    out=abs(31-pos.real)+abs(39-pos.imag)
    return(out)
    #return(min(out,1)) #BFS

def safe(pos): #Determine whether a pos is safe
    x=pos.real
    y=pos.imag
    z=int(x*x+3*x+2*x*y+y+y*y)+1350
    b=str(bin(z))[2:] #Binary representation
    c=b.count('1')
    if c%2==1:
        return(False) #If odd number of ones, space is wall
    elif c%2==0:
        return(True) #If even number of ones, space is open

def getChildren(node): #Produce a list of all possible children (next steps) of node
    pos=node.pos
    out=[]
    for d in [1,1j,-1,-1j]:
        new=pos+d
        if safe(new) and min(new.real,new.imag)>=0: #Negative values are not valid
            out.append(Node(parent=node,pos=new,path=node.path+[new]))
    return(out)

def prMaze(start=complex(1,1),end=complex(31,39),dim=45,path=[]): #Print maze
    top='   '
    pLen=0
    for y in range(dim):
        top+=str(y%10)
    print(top) #Print top row
    for y in range(dim):
        if y<10:
            line=str(y)+'  '
        else:
            line=str(y)+' '
        for x in range(dim):
            pos=complex(x,y)
            if pos==start:
                a='S'
            elif pos==end:
                a='E'
                pLen+=1
            elif pos in path:
                a='P'
                pLen+=1
            elif safe(pos):
                a='.'
            elif not safe(pos):
                a='#'
            line+=a
        print(line)
    if len(path)>0:
        print(str(pLen)+' steps')

retA=astar(input)
prMaze(path=retA.path)
#prMaze()