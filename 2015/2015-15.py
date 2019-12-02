#Advent of Code 2015 Day 15

import re
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-15.txt')
contents = f.read()
input = contents.splitlines()

def imp(input):
    ings={}
    for each in input:
        s=re.split(': |, ',each)
        ings[s[0]]={} #Create a sub-dict for each ingredient
        for i in range(len(s)-1):
            prop=s[i+1].split(' ')[0]
            val=int(s[i+1].split(' ')[1])
            ings[s[0]][prop]=val
        
    return(ings)

ings=imp(input)

def score(ings,amounts):
    iList=list(ings.keys())
    props=['capacity','durability','flavor','texture']
    scores=1 #Product of summed property scores
    for p in props:
        sum=0
        for i in ings: #Sum property values over all ingredients
            sum+=ings[i][p]*amounts[iList.index(i)]
        scores*=max(sum,0)
        #print(p+': '+str(sum))
    return(scores)
    
s=score(ings,[1,1,1,1])

def solveA(ings):
    mScore=0
    for x in range(101):
        for y in range(101-x):
            for z in range(101-y):
                s=score(ings,[x,y,z,100-x-y-z])
                if s>mScore:
                    mScore=s
                    print(str(s)+' '+str([x,y,z,100-x-y-z]))
    return(mScore)

retA=solveA(ings)
                
    