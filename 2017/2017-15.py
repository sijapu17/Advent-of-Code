#Advent of Code 2017 Day 15

val0=[873,583] #Starting values of A and B
mfact=[16807,48271] #Multiplipcation factors of A and B
div=2147483647 #Divide by this each time to find remainder
crit=[4,8] #Part B: consider only values which are multiples of these

def binlo16(n): #Return lowest 16 binary bits of a number
    bn=bin(n)[2:].zfill(16) #Convert to binary and zero-fill to reach at least 16 bits
    return(bn[-16:]) #Return last 16 bits

def step(val,mfact,div):
    valout=[]
    for i in range(len(val)):
        rem=(val[i]*mfact[i])%div
        valout.append(rem)
    return(valout)
    
def solveA(val0,mfact,div,reps):
    val=val0
    sum=0
    for n in range(reps): #Number of repetitions
        if n%1000000==0:
            print('Step '+str(n))
        val=step(val,mfact,div)
        if binlo16(val[0])==binlo16(val[1]):
            sum+=1
    return(sum)

#retA=solveA(val0,mfact,div,40000000)

def stepB(val,mfact,div,crit):
    valout=[]
    for i in range(len(val)):
        metCrit=False
        valu=val[i]
        while metCrit==False:
            valu=(valu*mfact[i])%div
            if valu%crit[i]==0:
                metCrit=True
        valout.append(valu)
    return(valout)

def solveB(val0,mfact,div,reps,crit):
    val=val0
    sum=0
    for n in range(reps): #Number of repetitions
        if n%50000==0:
            print('Step '+str(n))
        val=stepB(val,mfact,div,crit)
        if binlo16(val[0])==binlo16(val[1]):
            sum+=1
    print('Complete')            
    return(sum)

retB=solveB(val0,mfact,div,5000000,crit)