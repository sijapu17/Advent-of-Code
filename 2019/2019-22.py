#Advent of Code 2019 Day 22

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-22.txt')
contents = f.read()
input = contents.splitlines()

def shuffle(size,input,n): #Shuffle deck by converting shuffle steps into y=mx+c linear transformations
    prnt=False
    if size<20: #If deck is small, print each step
        prnt=True
        print(list(range(size)))
    m,c=1,0 #Starting position: y=x
    for step in input:
        if prnt:
            print(step)
        if step=='deal into new stack':
            m*=-1
            c=(-c+size-1)%size
        elif 'cut' in step:
            mag=int(step.split()[1])
            c=(c-mag)%size
        elif 'deal with increment' in step:
            mag=int(step.split()[3])
            m=(m*mag)%size
            c=(c*mag)%size
        else:
            print('Warning: step not recognised: '+step)
        if prnt:
            print([(m*x+c)%size for x in range(size)])
    return((m*n+c)%size)
            
retA=shuffle(10007,input,2019)

def modularInverse(mag,size): #Return modular inverse of mag mod size
    return(pow(mag,size-2,size))

def inverseShuffle(size,input,pos,nReps): #Shuffle deck backwards to find which card ends up in position pos
    prnt=False
    if size<20: #If deck is small, print each step
        prnt=True
        print(list(range(size)))
    m,c=1,0 #Starting position: y=x
    for step in reversed(input):
        if prnt:
            print(step)
        if step=='deal into new stack':
            m*=-1
            c=(-c+size-1)%size
        elif 'cut' in step:
            mag=int(step.split()[1])
            c=(c+mag)%size
        elif 'deal with increment' in step:
            mag=int(step.split()[3])
            m=(m*modularInverse(mag,size))%size
            c=(c*modularInverse(mag,size))%size
        else:
            print('Warning: step not recognised: '+step)
        if prnt:
            print([(m*x+c)%size for x in range(size)])
    ret=(pow(m,nReps,size)*pos + (pow(m,nReps,size)-1)*modularInverse(m-1,size)*c) % size
    return(ret)

retB=inverseShuffle(119315717514047,input,2020,101741582076661)