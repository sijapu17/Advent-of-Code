#Advent of Code 2023 Day 16

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-16.txt')
contents = f.read()
input = contents.splitlines()

map={}
x_max=len(input[0])
y_max=len(input)

#Import map
for j in range(y_max):
    for i in range(x_max):
        map[complex(i,j)]=input[j][i]

def in_range(pos:complex):
    return(0<=pos.real<x_max and 0<=pos.imag<y_max)

def count_energised(start):
    visited=set() #Log of (pos,vel) pairs which have already been visited
    frontier=[] #Stack of beams yet to be resolved

    frontier.append((start)) #Starting beam

    #Resolve beams
    while len(frontier)>0:
        current=frontier.pop()
        while in_range(current[0]) and current not in visited:
            visited.add(current)
            pos=current[0]
            vel=current[1] 
            match map[pos]: #Find current map tile
                case '/':
                    vel=complex(-1*vel.imag,-1*vel.real)
                    current=(pos+vel,vel)
                case '\\':
                    vel=complex(vel.imag,vel.real)
                    current=(pos+vel,vel)
                case '|':
                    if vel.imag==0: #Horizontal movement - continue down beam, and add up beam to frontier
                        frontier.append((pos+complex(0,-1),complex(0,-1)))
                        current=(pos+complex(0,1),complex(0,1))
                    else:
                        current=(pos+vel,vel)
                case'-':
                    if vel.real==0: #Vertical movement - continue right beam, and add left beam to frontier
                        frontier.append((pos+complex(-1,0),complex(-1,0)))
                        current=(pos+complex(1,0),complex(1,0))
                    else:
                        current=(pos+vel,vel)
                case _:
                    current=(pos+vel,vel)

    return(len(set([x[0] for x in visited]))) #Count number of visited positions

def best_start(): #Find best starting point for beam
    best=0 #Best number of beams energised
    for i in range(x_max):
        best=max(best,count_energised((complex(i,0),complex(0,1))))
        best=max(best,count_energised((complex(i,y_max-1),complex(0,-1))))
    for j in range(y_max):
        best=max(best,count_energised((complex(0,j),complex(1,0))))
        best=max(best,count_energised((complex(x_max-1,j),complex(-1,0))))        
    return(best)

#print(count_energised((0,complex(1,0))))
print(best_start())