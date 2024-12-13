#Advent of Code 2024 Day 12

from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-12.txt')
contents = f.read()
input = contents.splitlines()

map=defaultdict(str)
x_max=len(input[0])
y_max=len(input)
dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))

#Import map
for j in range(y_max):
    for i in range(x_max):
        map[complex(i,j)]=input[j][i]

def man_dist(c1:complex,c2:complex): #Return Manhatten Distance
    return(int(abs(c1.real-c2.real)+abs(c1.imag-c2.imag)))

total_price=0
discounted_price=0
visited=set()
#Loop through field, finding each region and calculating perimeter and area
for j in range(y_max):
    for i in range(x_max):
        pos=complex(i,j)
        val=map[pos]
        if pos not in visited:
            perimeter=0 #Length of perimeter in squares
            side_pieces=set() #Contiguous sides
            area=0
            #DFS to find all plants in region
            frontier=[pos]
            while len(frontier)>0:
                current=frontier.pop()
                if current in visited:
                    continue
                visited.add(current)
                area+=1
                for d in dirs:
                    new_pos=current+d
                    if map[new_pos]!=val: #If neighbour is a different plant (or off map), add 1 to perimeter
                        perimeter+=1
                        side_pieces.add((d,current)) #Record side pieces as tuple of direction and position
                    elif new_pos not in visited:
                        frontier.append(new_pos)
            total_price+=(perimeter*area) #Part 1
            sides=0
            for s in side_pieces: #For each piece, check if adjoining piece exists to avoid double-counting
                if (s[0],s[1]+s[0]*complex(0,1)) not in side_pieces:
                    sides+=1
            discounted_price+=(sides*area) #Part 2

print(total_price)
print(discounted_price)