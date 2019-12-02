#Advent of Code 2015 Day 5

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2015-5.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    sum=0
    for l in input:
        #Rule 1
        vct=0
        for v in 'aeiou':
            vct+=l.count(v)
        #Rule 2
        cct=0
        for c in range(len(l)-1):
            if l[c]==l[c+1]:
                cct=1
        #Rule 3
        if vct>=3 and cct==1:
            status=1
            for tu in ['ab','cd','pq','xy']:
                if tu in l:
                    status=0
            sum+=status
    return(sum)

#retA=solveA(input)
            
def solveB(input):
    sum=0
    for l in input:
        chk1=0
        chk2=0
        for j in range(len(l)-2):
            if l[j:j+2] in l[j+2:]:
                chk1=1
            if l[j]==l[j+2]:
                chk2=1
        if chk1+chk2==2:
            sum+=1
    return(sum)
            
retB=solveB(input)            