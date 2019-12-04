#Advent of Code 2017 Day 17

step=394
#nreps=2017
nreps=50000000

def solveA(step,nreps):
    buffer=[0]
    pos=0
    for n in range(1,nreps+1):
        pos=(pos+step)%n
        buffer.insert(pos+1,n)
        pos=(pos+1)%(n+1)
    posLast=buffer.index(nreps)
    afterLast=buffer[(posLast+1)%(nreps+1)]
    return(afterLast)

#testA=solveA(3,9)
#retA=solveA(step,nreps)

def solveB(step,nreps):
    pos=0
    pos1=0 #Keep track of number after 0
    for n in range(1,nreps+1):
        if n%500000==0:
            print('Step '+str(n))
        pos=(pos+step)%n
        if pos==0:
            pos1=n
        pos=(pos+1)%(n+1)
    return(pos1)

#testB=solveB(3,9)
retB=solveB(step,nreps)