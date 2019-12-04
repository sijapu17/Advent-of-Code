#Advent of Code 2018 Day 4

from collections import defaultdict
import re
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-4.txt')
contents = f.read()
input = sorted(contents.splitlines())

def solveA(input):
    p1=re.compile('\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] Guard #(\d+) begins shift')
    p2=re.compile('\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\] falls asleep')
    p3=re.compile('\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\] wakes up')
    id=0 #Guard ID
    #maxTime=0
    #maxID=0
    guards=defaultdict(lambda : defaultdict(int)) #Create a nested dict for each guard
    mostAsleep=defaultdict(int) #Create a dict to track total sleep for each guard
    for i in input:
        if p1.match(i): #First entry of evening
            m1=p1.match(i)
            id=int(m1.group(1))
        elif p2.match(i):
            m2=p2.match(i)
            slptime=int(m2.group(1)) #FInd sleep time, to use when guard wakes up
        elif p3.match(i):
            m3=p3.match(i)
            waketime=int(m3.group(1))
            for t in range(slptime,waketime):
                guards[id][t]+=1

            mostAsleep[id]+=waketime-slptime
    maxID=max(mostAsleep, key=mostAsleep.get) #ID of guard who sleeps most
    commonTime=max(guards[maxID],key=guards[maxID].get)
    print('Guard '+str(maxID)+' time '+str(commonTime))
    return(maxID*commonTime)
    
retA=solveA(input)
#24643 (1297 19) too low

def solveB(input):
    p1=re.compile('\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\] Guard #(\d+) begins shift')
    p2=re.compile('\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\] falls asleep')
    p3=re.compile('\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})\] wakes up')
    id=0 #Guard ID
    #maxTime=0
    #maxID=0
    guards=defaultdict(lambda : defaultdict(int)) #Create a nested dict for each guard
    for i in input:
        if p1.match(i): #First entry of evening
            m1=p1.match(i)
            id=int(m1.group(1))
        elif p2.match(i):
            m2=p2.match(i)
            slptime=int(m2.group(1)) #FInd sleep time, to use when guard wakes up
        elif p3.match(i):
            m3=p3.match(i)
            waketime=int(m3.group(1))
            for t in range(slptime,waketime):
                guards[id][t]+=1
    maxTime=0
    maxId=0
    maxMin=0
    for g in guards:
        t=max(guards[g],key=guards[g].get)
        v=guards[g][t]
        if v>maxTime:
            maxTime=v
            maxID=g
            maxMin=t
        
            
    print('Guard '+str(maxID)+' time '+str(maxMin))
    return(maxID*maxMin)
    
retB=solveB(input)