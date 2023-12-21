#Advent of Code 2023 Day 14

from itertools import pairwise

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-14.txt')
contents = f.read()
input = contents.splitlines()

cubes=[] #List of cube-shaped stationary rocks
rocks=set() #Set of round movable rocks

#Find coords of all cubes and rocks
for j in range(len(input)):
    for i in range(len(input[j])):
        match input[j][i]:
            case '#':
                cubes.append(complex(i,j))
            case 'O':
                rocks.add(complex(i,j))

#Indices of cube rows on each column
cube_cols=[]
for j in range(len(input)):
    col=[int(x.imag) for x in cubes if int(x.real)==j]
    cube_cols.append([-1]+col+[len(input)]) #Add dish walls as cubes

#Indices of cube column on each row
cube_rows=[]
for i in range(len(input[0])):
    row=[int(x.real) for x in cubes if int(x.imag)==i]
    cube_rows.append([-1]+row+[len(input[0])]) #Add dish walls as cubes

def print_dish(): #Print out map of dish
    ret=''
    for j in range(len(input)):
        for i in range(len(input[j])):
            x=complex(i,j)
            if x in cubes:
                ret+='#'
            elif x in rocks:
                ret+='O'
            else:
                ret+='.'
        ret+='\n'
    print(ret)

def tilt_dish(dir):
    #North or South, tilt within cols
    if dir in ('N','S'):
        for i in range(len(input[0])):
            #Look between each pair of cubes
            for a,b in pairwise(cube_cols[i]):
                if b-a>1:
                    #Count number of rocks in gap
                    n_rocks=len([x for x in rocks if int(x.real)==i and a<int(x.imag)<b])
                    for j in range(a+1,b):
                        if dir=='N':
                            if j<=a+n_rocks: #Add n_rocks rocks to top of gap
                                rocks.add(complex(i,j))
                            else: #Remove rocks from bottom of gap
                                rocks.discard(complex(i,j))
                        elif dir=='S':
                            if j>=b-n_rocks: #Add n_rocks rocks to bottom of gap
                                rocks.add(complex(i,j))
                            else: #Remove rocks from top of gap
                                rocks.discard(complex(i,j))

    #East or West, tilt within rows
    elif dir in ('W','E'):
        for j in range(len(input)):
            #Look between each pair of cubes
            for a,b in pairwise(cube_rows[j]):
                if b-a>1:
                    #Count number of rocks in gap
                    n_rocks=len([x for x in rocks if int(x.imag)==j and a<int(x.real)<b])
                    for i in range(a+1,b):
                        if dir=='W':
                            if i<=a+n_rocks: #Add n_rocks rocks to left of gap
                                rocks.add(complex(i,j))
                            else: #Remove rocks from right of gap
                                rocks.discard(complex(i,j))
                        elif dir=='E':
                            if i>=b-n_rocks: #Add n_rocks rocks to right of gap
                                rocks.add(complex(i,j))
                            else: #Remove rocks from left of gap
                                rocks.discard(complex(i,j))

def run_cycle(): #Run a spin cycle of N,W,S,E tilts
    for d in 'N','W','S','E':
        tilt_dish(d)

def load(rocks): #Calculate load
    return(sum([len(input)-int(x.imag) for x in rocks]))

def run_cycle_n(n): #Find rock positions after n spins by finding a cycle in the states
    rock_states={} #Dict of different rock states encountered
    c=0
    while c<n:
        c+=1
        run_cycle()
        if frozenset(rocks) in rock_states:
            c0=rock_states[frozenset(rocks)]
            cycle=c-c0 #Length of cycle
            b=(n-c0)%cycle #Offset from start of cycle to n
            print(f'Cycle length={cycle}')
            for i in range(b):
                run_cycle()
            return()
        #If rock state is new, add to dict
        rock_states[frozenset(rocks)]=c

print_dish()
tilt_dish('N')
print(load(rocks))
run_cycle_n(1000000000)
print_dish()
print(load(rocks))