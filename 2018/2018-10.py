#Advent of Code 2018 Day 10
import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-10.txt')
contents = f.read()
input=contents.splitlines()

def dataIn(input): #Parse coordinates
    p1=re.compile('position=<([ |-]\d+), ([ |-]\d+)> velocity=<([ |-]\d+), ([ |-]\d+)>')
    points=[]
    for each in input:
        m1=p1.match(each)
        coords=(int(m1.group(1)),int(m1.group(2)),int(m1.group(3)),int(m1.group(4)))
        points.append(coords)
    return(points)

points=dataIn(input)

def solveA(points):
    t=0
    best=None
    minHeight=float('Inf')
    while True:
        if t%500==1:
            print('t='+str(t))
        sky=set()
        for p in points:
            sky.add(complex((p[0]+t*p[2]),(p[1]+t*p[3])))
        height=max(x.imag for x in sky)-min(x.imag for x in sky)
        if height>minHeight:
            print('t='+str(t-1))
            return(best)
        minHeight=height
        best=sky
        t+=1
    
retA=solveA(points)

def displaySky(stars):
    ret=''
    minX=min(r.real for r in stars)
    maxX=max(r.real for r in stars)
    minY=min(r.imag for r in stars)
    maxY=max(r.imag for r in stars)
    for j in range(int(minY),int(maxY)+1):
        for i in range(int(minX),int(maxX)+1):
            if complex(i,j) in stars:
                ret+='#'
            else:
                ret+='.'
        ret+='\n'
    print(ret)
    
displaySky(retA)