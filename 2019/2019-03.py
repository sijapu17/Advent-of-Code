#Advent of Code 2019 Day 3

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-03.txt')
contents = f.read().splitlines()
input = [x.split(',') for x in contents]
inputTest = [['R8','U5','L5','D3'],['U7','R6','D4','L4']]

##### Part A #####

def getPoints(path): #Create a set of all points that the wire touches:
    pos=0j #Starting position
    points=set()
    dirs={'U':1j,'D':-1j,'R':1,'L':-1} #Conversion from UDLR to complex coordinate directions
    for b in path: #Traverse each bearing in the wire path
        dr=dirs[b[0]] #Direction of bearing
        mg=int(b[1:]) #Magnitude of bearing
        for i in range(mg): #Add each step along the bearing to the set
            pos+=dr
            points.add(pos)
    return(points)

def getCrossings(wires): #Find crossing points of two wires
    s=[]
    s.append(getPoints(wires[0]))
    s.append(getPoints(wires[1]))
    return(s[0].intersection(s[1]))

def ManDist(c): #Manhatten distance of a complex number
    return(int(abs(c.real)+abs(c.imag)))

def nearestCrossing(wires): #Find the Manhatten distance of closest crossing to the origin
    c=getCrossings(wires)
    closest=min(c,key=ManDist) #Find crossing with smallest Manhatten distance
    return(ManDist(closest))
    
retA=nearestCrossing(input)

##### Part B #####

def getPointTimes(path): #Create a dict of the earliest time that the wire touches each point:
    pos=0j #Starting position
    time=0 #Starting time
    points={}
    dirs={'U':1j,'D':-1j,'R':1,'L':-1} #Conversion from UDLR to complex coordinate directions
    for b in path: #Traverse each bearing in the wire path
        dr=dirs[b[0]] #Direction of bearing
        mg=int(b[1:]) #Magnitude of bearing
        for i in range(mg): #Add each step along the bearing to the set
            time+=1
            pos+=dr
            if pos not in points: #Store current time only if point has not been visited before
                points[pos]=time
    return(points)

def earliestCrossing(wires): #Find earliest crossing point
    times=[]
    times.append(getPointTimes(wires[0]))
    times.append(getPointTimes(wires[1]))
    crossings={}
    for t in times[0]:
        if t in times[1]: #If point is a crossing, store summed time of both wires
            crossings[t]=times[0][t]+times[1][t]
    earliest=min(crossings,key=lambda x:crossings[x])
    return(crossings[earliest])

retB=earliestCrossing(input)