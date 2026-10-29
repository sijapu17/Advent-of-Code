#Advent of Code 2025 Day 8
from itertools import combinations
import heapq

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-08.txt')
contents = f.read()
input=[x.split(',') for x in contents.splitlines()]

#Calculate square of Euclidean distance (no need to sqrt as this won't change ordering)
def sqr_euclidean_dist(a,b):
    return(int((a.x-b.x)**2+(a.y-b.y)**2+(a.z-b.z)**2))

class Junction_Box():
    def __init__(self,ID,coords):
        self.x, self.y, self.z = [int(a) for a in coords]
        self.ID=ID

    def __lt__(self,other):
        return(self.ID<other.ID)

    def __repr__(self) -> str:
        return(f'J{self.ID}: {self.x, self.y, self.z}')
    def __str__(self) -> str:
        return(self.__repr__())

class Circuit():
    def __init__(self,connections,box_ID):
        self.boxes=set()
        boxes_to_process=[box_ID] #Initial box
        #Iterate through all connected junction boxes
        while len(boxes_to_process)>0:
            current=boxes_to_process.pop()
            self.boxes.add(current)
            boxes_processed.add(current)
            for c in connections:
                if c[1]==current and c[2] not in boxes_processed:
                    boxes_to_process.append(c[2])
                elif c[2]==current and c[1] not in boxes_processed:
                    boxes_to_process.append(c[1])
        
        self.size=len(self.boxes)
    
    def __lt__(self,other):
        return(self.size<other.size)
    

boxes=[Junction_Box(ID,c) for ID,c in enumerate(input)]

dists=[] #Heap of distances
for a,b in combinations(boxes,2):
    heapq.heappush(dists,(sqr_euclidean_dist(a,b),a.ID,b.ID))

global boxes_processed
boxes_processed=set()

connections=heapq.nsmallest(1000,dists) #1000 shortest connections

circuits=[] #Heap of connected circuits
for b in boxes:
    if b.ID not in boxes_processed:
        heapq.heappush(circuits,Circuit(connections,b.ID))

largest_circuits=[x.size for x in heapq.nlargest(3,circuits)]
print(f'{largest_circuits} prod={largest_circuits[0]*largest_circuits[1]*largest_circuits[2]}')

#Part 2: Find last required connection for full connection
#Binary sort
n_lower=1000
n_upper=10000
while True:
    boxes_processed=set()
    n_mid=int((n_upper+n_lower)/2)
    connections_2=heapq.nsmallest(n_mid,dists) #n shortest connections

    circuits_2=[] #Heap of connected circuits
    for b in boxes:
        if b.ID not in boxes_processed:
            heapq.heappush(circuits_2,Circuit(connections_2,b.ID))
    
    print(f'n={n_mid}: {len(circuits_2)} circuits. {n_lower},{n_upper}')
    if n_lower==n_upper:
        c=connections_2[-1]
        print(boxes[c[1]].x*boxes[c[2]].x)
        print(connections_2[-1])
        break
    if len(circuits_2)==1:
        n_upper=n_mid
    elif len(circuits_2)>1:
        n_lower=max(n_mid,n_lower+1)
