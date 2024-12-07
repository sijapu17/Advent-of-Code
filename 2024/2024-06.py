#Advent of Code 2024 Day 6

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-06.txt')
contents = f.read()
input = contents.splitlines()

obstacles=set() #Coords of obstacles
x_max=len(input[0])
y_max=len(input)
goal = complex(x_max-1,y_max-1)

#Import map
for j in range(y_max):
    for i in range(x_max):
        if input[j][i]=='#':
            obstacles.add(complex(i,j))
        elif input[j][i]=='^':
            start_pos=complex(i,j)
            start_dir=complex(0,-1) #Facing upwards

def in_range(pos:complex):
    return(0<=pos.real<x_max and 0<=pos.imag<y_max)

def count_visited():
    global seen
    pos=start_pos
    dir=start_dir
    visited=set()
    seen=set() #All positions that the guard sees on their initial patrol - added obstacle for part 2 can only go here
    visited.add(pos)
    while in_range(pos):
        if in_range(pos+dir):
            seen.add(pos+dir)
        if pos+dir in obstacles: #Turn right if there is an obstacle in the way
            dir*=complex(0,1)
        else:
            pos+=dir
            if in_range(pos):
                visited.add(pos)
    return(len(visited))

print(count_visited())

def check_for_loop(new_ob): #Check if a block added at given position results in a loop
    pos=start_pos
    dir=start_dir
    visited=set()
    visited.add((pos,dir))
    while in_range(pos):
        if pos+dir in obstacles or pos+dir==new_ob: #Turn right if there is an obstacle in the way
            dir*=complex(0,1)
        else:
            pos+=dir
            if (pos,dir) in visited:
                return(True) #Return True if loop detected
            else:
                visited.add((pos,dir))
    return(False) #Return False if path exits map without looping   

print(sum([check_for_loop(p) for p in seen]))