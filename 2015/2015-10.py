#Advent of Code 2015 Day 10

input='1113122113'

def solveA(input,nreps):
    for n in range(nreps):
        print('Step '+str(n))
        i=0 #Position through string
        j=1 #Number of consecutive letters
        out=''
        input+='x' #Dummy character to avoid falling off end of string
        while i<len(input)-1:
            if input[i]==input[i+1]:
                j+=1
            else:
                out+=str(j)
                out+=input[i]
                j=1
            i+=1
        input=out
    return(len(input))

retA=solveA(input,50)