#Advent of Code 2016 Day 9

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-9.txt')
input = f.read()


def solveA(input):
    i=0
    l=len(input)
    out=''
    while i<l:
        print('i='+str(i))
        if input[i]!='(':
            out+=input[i]
            i+=1
        else:
            j=input[i:].find(')')
            code=input[i+1:i+j]
            i+=len(code)+2
            rptlen=int(code.split('x')[0]) #Length of repeating sequence
            rptn=int(code.split('x')[1]) #Number of repeats
            out+=input[i:i+rptlen]*rptn
            i+=rptlen
    return(len(out))

#input='X(8x2)(3x3)ABCY'
#retA=solveA(input)


def solveB(input,level):
    sum=0
    #print('Level '+str(level))
    while True:
        l=len(input)
        if level<=1:
            print('Level '+str(level)+' l='+str(l))
            #print(input)
        bpos=input.find('(')
        if bpos==-1: #Case where nothing left to decode
            sum+=l
            return(sum)
        elif bpos!=0: #Case where chars are before next brackets
            sum+=bpos
            input=input[bpos:]
            l=len(input)
        else:
            j=input.find(')')
            code=input[1:j]
            lcode=len(code)+2 #Length of code plus brackets
            rptlen=int(code.split('x')[0]) #Length of repeating sequence
            rptn=int(code.split('x')[1]) #Number of repeats
            sum+=solveB(input[lcode:lcode+rptlen]*rptn,level+1) #Recurse the expanded section
            input=input[lcode+rptlen:]

#input='X(8x2)(3x3)ABCY'
#input='X(3x3)ABC(3x3)ABCY'
#input='(1x2)XYZ'
retB=solveB(input,0)