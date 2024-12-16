#Advent of Code 2024 Day 15

from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-15.txt')
contents = f.read()
input = contents.splitlines()
in_map=input[:input.index('')]
instructions=''.join(input[input.index('')+1:])
dirs={'>':complex(1,0),'<':complex(-1,0),'v':complex(0,1),'^':complex(0,-1)}

#Import map
def import_map(in_map):
    map=defaultdict(str)
    x_max=len(in_map[0])
    y_max=len(in_map)
    walls=set()
    boxes=set()
    for j in range(y_max):
        for i in range(x_max):
            sym=in_map[j][i]
            if sym=='#':
                walls.add(complex(i,j))
            elif sym=='O':
                boxes.add(complex(i,j))
            elif sym=='@': #Robot position
                pos=complex(i,j)
    return(walls,boxes,pos)
#Part 1
walls1,boxes1,pos1=import_map(in_map)

#Make moves
for i in instructions:
    newpos=pos1+dirs[i]
    while newpos not in walls1: #If wall reached before an empty space is found, no movement occurs
        if newpos in boxes1: #If box, look ahead to see if next space
            newpos+=dirs[i]
        else: #Move in empty space
            if pos1+dirs[i] in boxes1: #Add box to furthest looked-at space and remove from nearest space (equivalent to pushing whole stack)
                boxes1.add(newpos)
                boxes1.remove(pos1+dirs[i])
            pos1+=dirs[i] #Move robot
            break

print(sum([int(c.real)+100*int(c.imag) for c in boxes1]))

#Part 2
def print_map(pos,l_boxes,r_boxes,walls):
    x_max=len(in_map2[0])
    y_max=len(in_map2)
    ret=''
    for j in range(y_max):
        for i in range(x_max):
            if complex(i,j) in l_boxes:
                ret+='['
            elif complex(i,j) in r_boxes:
                ret+=']' 
            elif complex(i,j) in walls:
                ret+='#'     
            elif complex(i,j)==pos:
                ret+='@' 
            else:
                ret+='.'
        ret+='\n'
    return(ret)

#Double map width
in_map2=[x.replace('#','##').replace('.','..').replace('O','O.').replace('@','@.') for x in in_map]
walls2,l_boxes2,pos2=import_map(in_map2)
r_boxes2={c+1 for c in l_boxes2}

#Make moves
for i in instructions:
    #Find all boxes to be moved
    queued_movers=set() #Boxes that have been processed, and will be moved unless a wall is hit
    frontier=[pos2+dirs[i]] #Box positions yet to be checked
    while len(frontier)>0:
        current=frontier.pop()
        if current in queued_movers:
            continue
        if current in walls2: #If a wall is hit, clear queued_movers and move to next instruction without moving any boxes
            queued_movers=set()
            break
        elif current in l_boxes2|r_boxes2:
            queued_movers.add(current)
            frontier.append(current+dirs[i])
            #If one side of box is processed, also process other side
            if current in l_boxes2:
                frontier.append(current+1)
            elif current in r_boxes2:
                frontier.append(current-1)
    #Move queued boxes
    l_remove=set() #Left boxes to remove
    l_add=set() #Left boxes to add
    for b in queued_movers:
        if b in l_boxes2:
            l_remove.add(b)
            l_add.add(b+dirs[i])
    l_boxes2-=l_remove
    l_boxes2|=l_add
    r_boxes2={c+1 for c in l_boxes2}
    #Move robot
    if current not in walls2:
        pos2+=dirs[i]

print(print_map(pos2,l_boxes2,r_boxes2,walls2))
print(sum([int(c.real)+100*int(c.imag) for c in l_boxes2]))
