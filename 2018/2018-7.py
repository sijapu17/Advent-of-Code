#Advent of Code 2018 Day 7

from collections import defaultdict
import re
import string

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-7.txt')
contents = f.read()
input = contents.splitlines()

def getSteps(input):
    p1=re.compile('Step (\w) must be finished before step (\w) can begin.')
    steps=[]
    for s in input:
        m1=p1.match(s)
        steps.append((m1.group(1),m1.group(2)))
    return(steps)

steps=getSteps(input)

def solveA(steps):
    letters=set()
    prereqs={}
    ret=''
    for s in steps: #Create list of all letters
        pre=s[0]
        post=s[1]
        letters.add(pre)
        letters.add(post)
    for l in letters: #Initialise a list of prereqs for each letter
        prereqs[l]=[]
    for s in steps: #Assign prereqs to steps
        pre=s[0]
        post=s[1]
        prereqs[post].append(pre)
    while len(ret)<len(letters): #Find letters with no outstanding prereqs and pick first alphabetically
        candidates=''
        for k, v in prereqs.items():
            if v==[]:
                candidates+=k
        next=sorted(candidates)[0]
        ret+=next
        for v in prereqs.values():
            if next in v:
                v.remove(next)
        del prereqs[next]
        
    return(ret)

#retA=solveA(steps)

def getAvailable(prereqs):
        candidates=[]
        for k, v in prereqs.items():
            if v==[]:
                candidates.append(k)
        return(sorted(candidates))

def solveB(steps,workers,dur):
    letters=set()
    prereqs={}
    completed=''
    available=[] #List of available jobs
    durs={} #Duration required to complete each task
    active={} #Jobs currently being worked on, and how long they have left to run
    idle=workers #Number of available workers
    time=0 #Elapsed seconds
    for s in steps: #Create list of all letters
        pre=s[0]
        post=s[1]
        letters.add(pre)
        letters.add(post)
    for l in letters: #Initialise a list of prereqs for each letter
        prereqs[l]=[]
        durs[l]=dur+1+string.ascii_uppercase.index(l)

    for s in steps: #Assign prereqs to steps
        pre=s[0]
        post=s[1]
        prereqs[post].append(pre)
    available=getAvailable(prereqs)
    while len(completed)<len(letters):
        cStep=[]
        for k, v in active.items(): #Check for any completed tasks
            if v==0:
                completed+=k
                cStep.append(k)
                print('T='+str(time)+' completed task '+str(k))
                idle+=1
                for val in prereqs.values():
                    if k in val:
                        val.remove(k)
                available=getAvailable(prereqs) #Update list of available tasks
        for c in cStep: #Remove completed tasks from active dict
            del active[c]
        while idle>0 and len(available)>0: #Assign open tasks to idle workers
            task=available.pop(0)
            active[task]=durs[task] #Assign correct duration to task on active dict
            del prereqs[task]
            idle-=1
        #Incremement times
        print('T='+str(time)+' Active'+str(active))
        time+=1 #Incremement times
        for k, v in active.items():
            active[k]=v-1
    time-=1 #Undo final time step
    return(time)        
    
#retB=solveB(steps,2,0)
retB=solveB(steps,5,60)