#Advent of Code 2016 Day 5

import hashlib

input='ffykfhsq'

def solveA(input):
    i=1
    pwrd=''
    l=0
    while l<8:
        if i%10000==1:
            print('Step '+str(i)+' '+pwrd)
        instr=input+str(i)
        m=hashlib.md5(instr.encode()).hexdigest()
        if m[:5]=='00000':
            pwrd+=m[5]
            l+=1
        i+=1
    return(pwrd)
        
#retA=solveA(input)

def solveB(input):
    i=1
    pwrd='--------'
    l=0
    while l<8:
        if i%100000==1:
            print('Step '+str(i)+' '+pwrd)
        instr=input+str(i)
        m=hashlib.md5(instr.encode()).hexdigest()
        if m[:5]=='00000' and m[5].isdigit():
            pos=int(m[5])
            if pos in range(8) and pwrd[pos]=='-':
                pwrd=pwrd[:pos]+m[6]+pwrd[pos+1:]
                l+=1
        i+=1
    return(pwrd)
        
retB=solveB(input)