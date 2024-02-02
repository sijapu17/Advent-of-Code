#Advent of Code 2023 Day 18


f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-18.txt')
contents = f.read()
input = contents.splitlines()

dirs={'U':complex(0,-1),'D':complex(0,1),'L':complex(-1,0),'R':complex(1,0)}
dir_ints={0:'R',1:'D',2:'L',3:'U'}
holes=set()

def dig_outline(input): #Dig out hole outline
    pos=0 #Current position
    holes.add(pos)
    for line in input:
        dir, d, col=line.split()
        for x in range(int(d)):
            pos+=dirs[dir]
            holes.add(pos)

def find_area_hex(input): #Find outline coords according to hex code
    pos=0 #Current position
    coords=[]
    perimeter=0
    for line in input:
        dir=dir_ints[int(line.split()[2][-2])]
        d=int(line.split()[2][2:7],16)
        pos+=d*dirs[dir]
        coords.append(pos)
        perimeter+=d #Calculate length of perimeter
    #Apply Shoelace formula
    coords.append(0) #Add origin to end of coordinates
    area=0
    for n in range(len(coords)-1):
        area+=int(coords[n].real*coords[n+1].imag-coords[n+1].real*coords[n].imag)
    final_area=int(abs(area/2)+perimeter/2+1)
    print(final_area)

def print_holes(holes):
    x_min=int(min([x.real for x in holes]))
    x_max=int(max([x.real for x in holes]))
    y_min=int(min([x.imag for x in holes]))
    y_max=int(max([x.imag for x in holes]))
    ret=''
    for j in range(y_min,y_max+1):
        for i in range(x_min,x_max+1):
            if complex(i,j) in holes:
                ret+='#'
            else:
                ret+='.'
        ret+='\n'
    print(ret)

def dig_area(): #Dig out hole inner
    #Start at 1 square SE of NW-most hole outline
    start_y=int(min([x.imag for x in holes]))
    start_x=int(min([x.real for x in holes if x.imag==start_y]))
    frontier=[]
    frontier.append(complex(start_x+1,start_y+1))
    i=0
    while len(frontier)>0:
        i+=1
        if i%100000==1:
            print(f'{i}: {len(frontier)}')
        current=frontier.pop()
        holes.add(current)
        for d in dirs.values():
            if current+d not in holes:
                frontier.append(current+d)
    print(len(holes))

#dig_outline(input)
#print_holes(holes)
#dig_area()
#print_holes(holes)
    
find_area_hex(input)