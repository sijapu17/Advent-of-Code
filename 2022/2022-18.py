#Advent of Code 2022 Day 18

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-18.txt')
contents = f.read()
inp = contents.splitlines()

class C3():
    def __init__(self,coords) -> None:
        self.x=int(coords[0])
        self.y=int(coords[1])
        self.z=int(coords[2])

    def __add__(self,other):
        return(C3((self.x+other.x,self.y+other.y,self.z+other.z)))

    def __radd__(self, other):
        return self.__add__(other)
    
    def __eq__(self, other) -> bool:
        return(self.x==other.x and self.y==other.y and self.z==other.z)
    
    def __hash__(self) -> int:
        return(hash((self.x,self.y,self.z)))

    def __str__(self) -> str:
        return(f'C({self.x},{self.y},{self.z})')
    
    def __repr__(self) -> str:
        return(self.__str__())

rocks=set()
for i in inp:
    rocks.add(C3(i.split(',')))

#Part 1: Find all sides of rocks which do not have a neighbour
sides_1=0
dirs=(C3((1,0,0)),C3((-1,0,0)),C3((0,1,0)),C3((0,-1,0)),C3((0,0,1)),C3((0,0,-1)))
#Loop across all neighbours of all rocks to find open sides
for r in rocks:
    for d in dirs:
        if r+d not in rocks:
            sides_1+=1
print(sides_1)

#Part 2: Find all rock sides which can be reached from the outside of the shape
sides_2=0
min_bound=C3((min(a.x for a in rocks),min(a.y for a in rocks),min(a.z for a in rocks)))
max_bound=C3((max(a.x for a in rocks),max(a.y for a in rocks),max(a.z for a in rocks)))

#Check whether a coordinate is inside bounds of a cuboid bounding all rock coords
def in_bounds(c:C3,min_b:C3,max_b:C3):
    return((min_b.x-1<=c.x<=max_b.x+1) and (min_b.y-1<=c.y<=max_b.y+1) and (min_b.z-1<=c.z<=max_b.z+1))

#DFS starting from a corner of bounding cuboid to find all rock sides that can be reached from the outside
stack=[]
visited=set()
stack.append(min_bound+C3((-1,-1,-1)))
while len(stack)>0:
    current=stack.pop()
    if current in visited:
        continue
    visited.add(current)
    for d in dirs:
        nghbr=current+d
        if nghbr in rocks:
            sides_2+=1
        elif in_bounds(nghbr,min_bound,max_bound) and nghbr not in visited:
            stack.append(nghbr)
print(sides_2)
