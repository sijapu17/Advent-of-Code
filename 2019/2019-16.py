#Advent of Code 2019 Day 16

from collections import deque

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-16.txt')
contents = f.read()

input=[int(x) for x in contents]

def runPhase(input): #Run one phase
    pattern=[0,1,0,-1]
    result=[]
    for i in range(1,len(input)+1): #Create pattern deque for the line
        linePattern=deque()
        for p in pattern: #Add pattern value the number of times specified by the line number
            for j in range(i):
                linePattern.append(p)
        res=0
        for d in input: #For each digit of input, multiply by pattern value
            linePattern.rotate(-1) #Offset by 1, as per FFT spec
            res+=(d*linePattern[0])
        result.append(abs(res)%10) #Only keep last digit
    return(result)

def solveA(input):
    num=input.copy()
    for i in range(100): #Run 100 phases
        num=runPhase(num)
    #Only keep first 8 digits
    retS=''
    for i in range(8):
        retS+=str(num[i])
    ret=int(retS)
    return(ret)

retA=solveA(input)

def runPhaseB(input): #As offset is >n/2 for part 2, digit i after FFT is just the sum of all digits >=i (mod 10)
    res=[]
    s=sum(input) #Start with full sum, and then subtract one value at a time
    for n in input:
        res.append(abs(s)%10)
        s-=n
    return(res)

def solveB(input):
    num=input*10000 #Repeat input 10000 times
    offset=int(''.join([str(x) for x in num[:7]])) #First 7 digits of input
    print('Offset='+str(offset))
    num1=num[offset:] #We only need to keep the input from the index specified by offset
    print(str(len(num1)))
    for i in range(1,101): #Run 100 phases
        #if i%10==1:
        print('Phase '+str(i))
        num1=runPhaseB(num1)
    #Only keep first 8 digits
    retS=''
    for i in range(8):
        retS+=str(num1[i])
    ret=int(retS)
    return(ret)

retB=solveB(input)       
        