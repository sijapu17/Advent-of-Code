#Advent of Code 2015 Day 3

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2015-3.txt')
contents = f.read()
#input = contents.splitlines()

def solveA(input):
    dir={}
    dir['>']=complex(1,0)
    dir['<']=complex(-1,0)
    dir['^']=complex(0,1)
    dir['v']=complex(0,-1)
    start=complex(0,0)
    posS=start
    posR=start
    vis=set()
    vis.add(start)
    i=0
    for d in input:
        if i==0:
            posS+=dir[d]
            vis.add(posS)
            i=1
        elif i==1:
            posR+=dir[d]
            vis.add(posR)
            i=0
    return(len(vis))

retA=solveA(contents)