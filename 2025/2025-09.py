#Advent of Code 2025 Day 9
from itertools import combinations

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-09.txt')
contents = f.read()
input=[[int(y) for y in x.split(',')] for x in contents.splitlines()]

def area(c1,c2): #Calculate area of rectangle between two points
    return((abs(c1[0]-c2[0])+1)*(abs(c1[1]-c2[1])+1))

def largest_area(input):
    max_area=0
    for a,b in combinations(input,2):
        if area(a,b)>max_area:
            max_area=area(a,b)
    return(max_area)

print(largest_area(input))

#Part 2: Create list of straight-line edges
edges=[]
for n in range(len(input)):
    edges.append((input[n][0],input[(n+1)%len(input)][0],input[n][1],input[(n+1)%len(input)][1]))

def collides(box,edge): #Check if box collides with edge
    x_overlap=min(edge[0],edge[1])<box[1] and box[0]<max(edge[0],edge[1])
    y_overlap=min(edge[2],edge[3])<box[3] and box[2]<max(edge[2],edge[3])
    return(x_overlap and y_overlap)

def largest_enclosed_area(input):
    max_area=0
    for a,b in combinations(input,2):
        #box is a tuple of (x0,x1,y0,y1)
        if area(a,b)>max_area:
            #If area is potentially largest, check collision with all edges
            collision=False
            box=(min(a[0],b[0]),max(a[0],b[0]),min(a[1],b[1]),max(a[1],b[1]))
            for e in edges:
                if collides(box,e):
                    collision=True
                    break
            if not collision:
                max_area=area(a,b)
    return(max_area)

print(largest_enclosed_area(input))
