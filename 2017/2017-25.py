#Advent of Code 2017 Day 25

def getVal(tape,pos): #Initialise tape if needed and return value
    if pos not in tape:
        tape[pos]=0
    return(tape[pos])

def SolveA(nreps):
    tape={} #Empty postitions on tape are 0
    pos=0
    state='A'
    for n in range(nreps):
        if n%100000==1:
            print('Step '+str(n))
        if state=='A':
            if getVal(tape,pos)==0:
                tape[pos]=1
                pos+=1
                state='B'
            else:
                pos-=1
                state='E'
        elif state=='B':
            if getVal(tape,pos)==0:
                tape[pos]=1
                pos+=1
                state='C'
            else:
                pos+=1
                state='F'
        elif state=='C':
            if getVal(tape,pos)==0:
                tape[pos]=1
                pos-=1
                state='D'
            else:
                tape[pos]=0
                pos+=1
                state='B'
        elif state=='D':
            if getVal(tape,pos)==0:
                tape[pos]=1
                pos+=1
                state='E'
            else:
                tape[pos]=0
                pos-=1
                state='C'
        elif state=='E':
            if getVal(tape,pos)==0:
                tape[pos]=1
                pos-=1
                state='A'
            else:
                tape[pos]=0
                pos+=1
                state='D'
        if state=='F':
            if getVal(tape,pos)==0:
                tape[pos]=1
                pos+=1
                state='A'
            else:
                pos+=1
                state='C'
    sum=0
    for t in tape:
        sum+=tape[t]
    return(sum)

retA=SolveA(12459852)
            
        
