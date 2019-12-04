#Advent of Code 2018 Day 16

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-16.txt')
contents = f.read()
input=contents.splitlines()
f2 = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-16b.txt')
contents2 = f2.read()
input2=contents2.splitlines()
import re

def addr(reg,a,b,c):
    reg[c]=reg[a]+reg[b]
def addi(reg,a,b,c):
    reg[c]=reg[a]+b
def mulr(reg,a,b,c):
    reg[c]=reg[a]*reg[b]
def muli(reg,a,b,c):
    reg[c]=reg[a]*b
def banr(reg,a,b,c):
    reg[c]=reg[a]&reg[b]   
def bani(reg,a,b,c):
    reg[c]=reg[a]&b
def borr(reg,a,b,c):
    reg[c]=reg[a]|reg[b]    
def bori(reg,a,b,c):
    reg[c]=reg[a]|b
def setr(reg,a,b,c):
    reg[c]=reg[a]    
def seti(reg,a,b,c):
    reg[c]=a
def gtir(reg,a,b,c):
    if a>reg[b]:
        reg[c]=1
    else:
        reg[c]=0
def gtri(reg,a,b,c):
    if reg[a]>b:
        reg[c]=1
    else:
        reg[c]=0
def gtrr(reg,a,b,c):
    if reg[a]>reg[b]:
        reg[c]=1
    else:
        reg[c]=0
def eqir(reg,a,b,c):
    if a==reg[b]:
        reg[c]=1
    else:
        reg[c]=0
def eqri(reg,a,b,c):
    if reg[a]==b:
        reg[c]=1
    else:
        reg[c]=0
def eqrr(reg,a,b,c):
    if reg[a]==reg[b]:
        reg[c]=1
    else:
        reg[c]=0
            
def parse(input):
    i=0
    j=0
    tests={}
    p1=re.compile('\w+:\s+(\[.+\])')
    p2=re.compile('(\d+) (\d+) (\d+) (\d+)')
    while i<len(input):
        m1=p1.match(input[i])
        tests[j]={}
        tests[j]['before']=eval(m1.group(1))
        i+=1
        m2=p2.match(input[i])
        tests[j]['args']=(int(m2.group(1)),int(m2.group(2)),int(m2.group(3)),int(m2.group(4)))
        i+=1
        m3=p1.match(input[i])
        tests[j]['after']=eval(m3.group(1))
        i+=2
        j+=1
    return(tests)
        
tests=parse(input)

def runTests(tests): #Run each instruction on the test case, and see how many tests pass at least three instructions
           
    fncs=(addr,addi,mulr,muli,banr,bani,borr,bori,setr,seti,gtir,gtri,gtrr,eqir,eqri,eqrr)
    count=0
    for t in tests.values():
        nPassed=0
        #print(t)
        for f in fncs:
            reg=t['before'][:]
            f(reg,t['args'][1],t['args'][2],t['args'][3])
            #print(str(f)+': '+str(reg))
            if reg==t['after']:
                nPassed+=1
        #print(str(nPassed))
            if nPassed>=3:
                count+=1
                break

    return(count)

#retA=runTests(tests)

def runTests(tests): #Run each instruction on the test case, and see how many tests pass at least three instructions
            
    fncs=(addr,addi,mulr,muli,banr,bani,borr,bori,setr,seti,gtir,gtri,gtrr,eqir,eqri,eqrr)
    fDict={}
    for f in fncs:
        fDict[f]=set(range(len(fncs)))
        
    for t in tests.values():
        for f in fncs:
            reg=t['before'][:]
            f(reg,t['args'][1],t['args'][2],t['args'][3])
            if reg!=t['after']:
                if t['args'][0] in fDict[f]:
                    fDict[f].remove(t['args'][0])
    return(fDict)

fDict=runTests(tests)

def refine(fDict):
    refinedDict={}
    while len(refinedDict)<len(fDict):
        for k,v in fDict.items():
            if len(v)==1:
                n=v.pop()
                refinedDict[n]=k
                for x in fDict.values():
                    if n in x:
                        x.remove(n)
                    #print(refinedDict)
    return(refinedDict)

refinedDict=refine(fDict)

def solveB(input2,refinedDict):
              
    reg=[0,0,0,0]
    p1=re.compile('(\d+) (\d+) (\d+) (\d+)')
    for x in input2:
        m1=p1.match(x)
        fNum=int(m1.group(1))
        fcn=refinedDict[fNum]
        #print(p1.group(2))
        fcn(reg,int(m1.group(2)),int(m1.group(3)),int(m1.group(4)))
    return(reg)

retB=solveB(input2,refinedDict)
        