#Advent of Code 2016 Day 1

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-1.txt')
contents = f.read()
input = contents.split(', ')

def solveA(input):
    
    pos=complex()
    dirs=(1,complex(0,-1),-1,complex(0,1))
    i=3
    
    for step in input:
        print(pos)
        print(step)
        if step[0]=='R':
            i=(i+1)%4
        elif step[0]=='L':
            i=(i-1)%4
        pos=pos+int(step[1:])*dirs[i]
        
    print(pos)
    return(abs(pos.real)+abs(pos.imag))

#retA=solveA(input)

def solveB(input):
    
    pos=complex()
    dirs=(1,complex(0,-1),-1,complex(0,1))
    i=3
    visited=[pos]
    
    for step in input:
        print(pos)
        print(step)
        if step[0]=='R':
            i=(i+1)%4
        elif step[0]=='L':
            i=(i-1)%4
        for j in range(int(step[1:])):
            pos=pos+dirs[i]
            if pos in visited:        
                print(pos)
                return(abs(pos.real)+abs(pos.imag))
            else:
                visited.append(pos)

retB=solveB(input)