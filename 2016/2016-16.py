#Advent of Code 2016 Day 16

input='10111011111001111'
fSize=272

def dragon(string): #One step of the dragon algorithm
    oppo={'1':'0','0':'1'}
    a0=string+'0'
    b=string[::-1]
    for i in b:
        a0+=oppo[i]
    return(a0)

def fillDisk(string,size):
    s=string
    while len(s)<size:
        print('Length '+str(len(s)))
        s=dragon(s)
    return(s[:size])

def checksum(string): #Compute checksum
    s=string
    while(len(s)%2==0): #If string has even length, perform checksum step
        print('Length '+str(len(s)))
        c=''
        for i in range(0,len(s),2):
            if s[i]==s[i+1]:
                c+='1'
            else:
                c+='0'
        s=c
    return(s)

def solveA(string,length):
    d=fillDisk(string,length)
    print('Disk filled')
    return(checksum(d))

#retA=solveA(input,fSize)
fSize2=35651584
retB=solveA(input,fSize2)