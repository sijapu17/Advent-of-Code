#Advent of Code 2016 Day 11
import string
import copy
from itertools import combinations
#input = [1,['p','P'],['O','U','R','L'],['o','u','r','l'],[]]
input2 = [1,['e','d','E','D','p','P'],['O','U','R','L'],['o','u','r','l'],[]]

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, status=None):
        self.status = status

        self.g = 0
        self.h = h(status)
        self.f = 0

    def __eq__(self, other):
        return self.status == other.status
    
    def __str__(self):
        return(str(self.status)+' g='+str(self.g)+' h='+str(self.h)+' f='+str(self.f))
    
    def __hash__(self):
        return(hash((str(self.status),self.g)))

def astar(input):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(encode(input))
    start_node.g = start_node.h = start_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()

    # Add the start node
    open_list.append(start_node)
    
    n=0

    # Loop until you find the end
    while len(open_list) > 0:# and n<4:
        
        n+=1
        #if n==60:
        #    return(closed_list)
        #print('Step '+str(n)+' Open List:')
        #for o in open_list:
        #      print(str(o))
        # Get the current node
        current_node = open_list[0]

        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.add(current_node)

        # Found the goal
        if n%50==1:
            print(str(n)+': Current node '+str(current_node))
        if h(current_node.status) == 0:
            print('Steps='+str(current_node.g))
            return(current_node)

        # Generate children
        children = getChildren(current_node.status)
        #print('Children '+str(children))
        # Loop through children
        for child in children:

            # Child is on the closed list
            seen=False
            for closed_child in closed_list:
                if child.status == closed_child.status:
                    seen=True

            if not seen:
                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = h(child.status)
                child.f = child.g + child.h

                # Child is already in the open list
                inOpen=False
                for open_node in open_list:
                    if child.status == open_node.status and child.g >= open_node.g:
                        inOpen=True

                if not inOpen:
                    # Add the child to the open list
                    open_list.append(child)
            
        open_list=[x for x in open_list if x not in closed_list]

def getFloor(status,letter): #Find floor which letter is on
    for f in range(1,5):
        if letter in status[f]:
            return(f)

def getGens(status,floor): #Return generators on floor
    azup=string.ascii_uppercase
    out=''
    for i in status[floor]:
        if i in azup:
            out+=i
    return(out)

def getChips(status,floor): #Return chips on floor
    azlo=string.ascii_lowercase
    out=''
    for i in status[floor]:
        if i in azlo:
            out+=i
    return(out)

def encode(status): #Encode status so equivalent statuses are considered as equal
    #print('Encoding '+str(status))
    az=string.ascii_lowercase
    i=0
    d={} #Dictionary for conversion
    out=[status[0],[],[],[],[]] #Maintain floor number
    for f in range(1,5): #Create dictionary
        for a in status[f]:
            if a not in d: #If not in dictionary yet
                d[a.lower()]=az[i].lower() #Assign microchip to first available letter in the alphabet
                d[a.upper()]=az[i].upper() #Assign corresponding generator
                i+=1
    for f in range(1,5): #Convert using dictionary
        for a in status[f]:
            out[f].append(d[a])
        out[f]=sorted(out[f])
    #STAGE 2a
    for f in range(1,5):
        gens=getGens(out,f)
        chips=gens.lower()
        if len(gens)>=2: #If there are at least 2 generators on a floor, sort their corresponding chips
            oldFloors=[] #List of floors that corresponding chips are on
            for c in chips:
                oldFloors.append(getFloor(out,c))
            newFloors=sorted(oldFloors)
            if newFloors!=oldFloors:
                for i in range(len(chips)): #Move chips from old to new floors
                    out[oldFloors[i]].remove(chips[i])
                    out[newFloors[i]].append(chips[i])
    #STAGE 2b
    for f in range(1,5):
        chips=getChips(out,f)
        gens=chips.upper()
        if len(chips)>=2: #If there are at least 2 generators on a floor, sort their corresponding chips
            oldFloors=[] #List of floors that corresponding chips are on
            for g in gens:
                oldFloors.append(getFloor(out,g))
            newFloors=sorted(oldFloors)
            if newFloors!=oldFloors:
                for i in range(len(gens)): #Move chips from old to new floors
                    out[oldFloors[i]].remove(gens[i])
                    out[newFloors[i]].append(gens[i])
    for f in range(1,5):
        out[f]=sorted(out[f])
    return(out)

def h(status): #Calculate h-value of status (i.e. minimum number of steps from current state to end
    out=(len(status[1])*3+len(status[2])*2+len(status[3]))/2
    return(out)

def safe(status): #Determine whether a status is safe
    for f in range(1,5):
        fCopy=status[f].copy()
        if len(fCopy)>0: #An empty floor is safe
            if fCopy[0]==fCopy[0].upper(): #If first item is a chip, all items are chips so floor is safe
                i=0
                while i<len(fCopy):
                    if fCopy[i]==fCopy[i].upper(): #If generator, sheild corresponding chip by removing it
                        if fCopy[i].lower() in fCopy:
                            fCopy.remove(fCopy[i].lower())
                        i+=1
                    else: #If chip is found then it hasn't been sheilded, so it will be destroyed
                        return(False)
    return(True) #If no floors are unsafe, status is safe

def getChildren(status): #Produce a list of all possible children (next steps) of status
    out=[]
    fNum=status[0]
    if fNum==1:
        nBelow=0
    else:
        nBelow=len(max(status[1:fNum],key=len)) #Number of items below current floor
    fContents=status[fNum]
    combs=[comb for i in range(2) for comb in combinations(fContents, i + 1)]
    for c in combs:
        if fNum<4: #If not at the top floor, try moving up
            newStatus=copy.deepcopy(status)
            newStatus[0]=fNum+1
            newStatus[fNum]=[x for x in fContents if x not in c] #Remove moved items from floor
            newStatus[fNum+1]+=c
            e=encode(newStatus)
            eNode=Node(status=e)
            if safe(e) and eNode not in out:
                out.append(eNode)
        if nBelow>0: #If items exist below, try moving down
            newStatus=copy.deepcopy(status)
            newStatus[0]=fNum-1
            newStatus[fNum]=[x for x in fContents if x not in c] #Remove moved items from floor
            newStatus[fNum-1]+=c
            e=encode(newStatus)
            eNode=Node(status=e)
            if safe(e) and eNode not in out:
                out.append(eNode)
    return(out)


#input = [1,['A','B'],['a','b'],[],[]]
#e=encode(input)
#c=children(input)
#s1=[4, [], ['A', 'B', 'C', 'D', 'E'], ['d'], ['a', 'b', 'c', 'e']]
#e1=encode(s1)
#n2=Node([2, [], ['A', 'B', 'C', 'D', 'E', 'a'], ['b', 'c', 'd', 'e'], []])
#c2=getChildren(n2.status)
#n4=Node([2, ['a'], ['A', 'B', 'C', 'D', 'E'], ['b', 'c', 'd', 'e'], []])
#c4=getChildren(n4.status)
#retA=astar(input)
retB=astar(input2)