#Advent of Code 2015 Day 11

from string import ascii_lowercase
input='vzbxkghb'
alpha=ascii_lowercase

def increment(input): #Increment password by 1
    i=len(input)-1
    pwrd=list(input)
    while True:
        if pwrd[i]=='z': #If z then increment letter to the left
            pwrd[i]='a'
            i-=1
        elif pwrd[i] in 'hkn': #Skip i,o,l
            pwrd[i]=alpha[alpha.index(pwrd[i])+2]
            break            
        else:
            pwrd[i]=alpha[alpha.index(pwrd[i])+1]
            break
    return(''.join(list(pwrd)))

def valid(input): #Check whether password is valid
    tre=False #Rule 1
    for i in range(len(input)-2):
        if input[i:i+3] in alpha:
            tre=True
            break
    if tre==False:
        return(False)
    for l in 'iol': #Rule 2
        if l in input:
            return(False)
    dub=0 #Rule 3
    i=0
    while i<len(input)-1:
        if input[i]==input[i+1]:
            dub+=1
            i+=2
        else:
            i+=1
    if dub>1:
        return(True)
    else:
        return(False)
    
def solveA(input):
    pwrd=input
    while True:
        pwrd=increment(pwrd)
        if valid(pwrd):
            return(pwrd)
        
retA=solveA(input)

retB=solveA(retA)
                 
        