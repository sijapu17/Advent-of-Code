#Advent of Code 2016 Day 14

import hashlib
input='ahsbgdzn'

def findThree(hash):
    for i in range(len(hash)-2):
        if hash[i]==hash[i+1]==hash[i+2]:
            return(hash[i])
    return(False)

def findFiveOf(hash,char):
    for i in range(len(hash)-4):
        if char==hash[i]==hash[i+1]==hash[i+2]==hash[i+3]==hash[i+4]:
            return(True)
    return(False)

def hashA(input,i):
    instr=input+str(i)
    m=hashlib.md5(instr.encode()).hexdigest()
    return(m)   

def hash(input,i):
    m=input+str(i)
    for n in range(2017):
        m=hashlib.md5(m.encode()).hexdigest()
    return(m)

def solveA(input):
    i=0 #Biggest index checked for 3 in a row
    hashed={}
    keys=[]
    nKeys=0
    while True:
        if i%1000==1:
            print('Step '+str(i))
        h=hash(input,i)
        hashed[i]=h
        c=findThree(h)
        if c:
            #print('Potential key '+str(i)+': '+str(h))
            k=i+1
            i1000=k+1000            
            found=False
            while k<i1000 and not found:
                #print('k='+str(k))
                if k in hashed:
                    h5=hashed[k] #Use results already hashed where available
                else:
                    h5=hash(input,k)
                    hashed[k]=h5
                if findFiveOf(h5,c):
                    keys.append(i)
                    nKeys+=1
                    found=True
                    print('Confirmed key '+str(i)+': '+str(h))
                    print('Key match '+str(k)+': '+str(h5))
                    print(str(nKeys)+' keys found')
                k+=1
        i+=1
        if nKeys==64:
            return(keys)

#input='abc'     
retA=solveA(input)