#Advent of Code 2016 Day 21

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-21.txt')
input = f.read().splitlines()
import re

def parse(input):
    p1=re.compile('swap position (\d+) with position (\d+)')
    p2=re.compile('swap letter (\w+) with letter (\w+)')
    p3=re.compile('rotate (left|right) (\d+) steps?')
    p4=re.compile('rotate based on position of letter (\w+)')
    p5=re.compile('reverse positions (\d+) through (\d+)')
    p6=re.compile('move position (\d+) to position (\d+)')
    ret=[]
    for s in input:
        instr={}
        if p1.match(s):
            m=p1.match(s)
            instr['type']='swapp'
            instr['pos1']=int(m.group(1))
            instr['pos2']=int(m.group(2))
        elif p2.match(s):
            m=p2.match(s)
            instr['type']='swapl'
            instr['let1']=m.group(1)
            instr['let2']=m.group(2)
        elif p3.match(s):
            m=p3.match(s)
            instr['type']='rotaten'
            dir=m.group(1)
            if dir=='left':
                dirn=1
            elif dir=='right':
                dirn=-1
            instr['n']=int(m.group(2))*dirn
        elif p4.match(s):
            m=p4.match(s)
            instr['type']='rotatep'
            instr['let1']=m.group(1)
        elif p5.match(s):
            m=p5.match(s)
            instr['type']='reverse'
            instr['pos1']=int(m.group(1))
            instr['pos2']=int(m.group(2))
        elif p6.match(s):
            m=p6.match(s)
            instr['type']='move'
            instr['pos1']=int(m.group(1))
            instr['pos2']=int(m.group(2))
        else:
            print(str(s)+' not parsed')
        ret.append(instr)
    return(ret)

instrs=parse(input)
pwrd='abcdefgh'
#pwrd='abcde'

def solveA(password,instrs):

    def swapp(pwrd,instr):
        i0=min(instr['pos1'],instr['pos2'])
        i1=max(instr['pos1'],instr['pos2'])
        return(pwrd[:i0]+pwrd[i1]+pwrd[i0+1:i1]+pwrd[i0]+pwrd[i1+1:])

    def swapl(pwrd,instr):
        pos1=pwrd.find(instr['let1'])
        pos2=pwrd.find(instr['let2'])
        return(swapp(pwrd,{'pos1':pos1,'pos2':pos2}))
        
    def rotaten(pwrd,instr):
        l=len(pwrd)
        n=instr['n']%l
        return(pwrd[n:]+pwrd[:n])

    def rotatep(pwrd,instr):
        pos=pwrd.find(instr['let1'])
        if pos>=4:
            pos+=1
        return(rotaten(pwrd,{'n':-1*(pos+1)}))

    def reverse(pwrd,instr):
        p1=min(instr['pos1'],instr['pos2'])
        p2=max(instr['pos1'],instr['pos2'])
        return(pwrd[:p1]+pwrd[p1:p2+1][::-1]+pwrd[p2+1:])

    def move(pwrd,instr):
        p1=instr['pos1']
        p2=instr['pos2']
        c=pwrd[p1]
        rem=pwrd[:p1]+pwrd[p1+1:]
        return(rem[:p2]+c+rem[p2:])
    
    funcs={'swapp':swapp,'swapl':swapl,'rotaten':rotaten,'rotatep':rotatep,'reverse':reverse,'move':move}
    pwrd=password[:]
    print(pwrd)
    for i in instrs:
        before=pwrd
        pwrd=funcs[i['type']](pwrd,i)
        print(before+' '+str(i)+' '+pwrd)
        
    print('Encoded: '+pwrd)
    return(pwrd)

retA=solveA(pwrd,instrs) #bcafeghd incorrect

def invert(pwrd,instrs): #Create list of instructions that inverts original instrs
    
    def swapp(pwrd,instr):
        i0=min(instr['pos1'],instr['pos2'])
        i1=max(instr['pos1'],instr['pos2'])
        return(pwrd[:i0]+pwrd[i1]+pwrd[i0+1:i1]+pwrd[i0]+pwrd[i1+1:])

    def swapl(pwrd,instr):
        pos1=pwrd.find(instr['let1'])
        pos2=pwrd.find(instr['let2'])
        return(swapp(pwrd,{'pos1':pos1,'pos2':pos2}))
        
    def rotaten(pwrd,instr):
        l=len(pwrd)
        n=instr['n']%l
        return(pwrd[n:]+pwrd[:n])

    def rotatep(pwrd,instr):
        pos=pwrd.find(instr['let1'])
        if pos>=4:
            pos+=1
        return(rotaten(pwrd,{'n':-1*(pos+1)}))

    def reverse(pwrd,instr):
        p1=min(instr['pos1'],instr['pos2'])
        p2=max(instr['pos1'],instr['pos2'])
        return(pwrd[:p1]+pwrd[p1:p2+1][::-1]+pwrd[p2+1:])

    def move(pwrd,instr):
        p1=instr['pos1']
        p2=instr['pos2']
        c=pwrd[p1]
        rem=pwrd[:p1]+pwrd[p1+1:]
        return(rem[:p2]+c+rem[p2:])
    
    funcs={'swapp':swapp,'swapl':swapl,'rotaten':rotaten,'rotatep':rotatep,'reverse':reverse,'move':move}
    iinstrs=[]
    instrsin=instrs.copy()
    while len(instrsin)>0:
        i=instrsin.pop()
        if i['type']=='swapp':
            iinstr=i
        elif i['type']=='swapl':
            iinstr=i
        elif i['type']=='rotaten':
            i['n']*=-1
            iinstr=i
        elif i['type']=='rotatep':
            rots={1:1,3:2,5:3,7:4,2:6,4:7,6:8,0:9}
            pos=pwrd.find(i['let1'])
            iinstr={'type':'rotaten','n':rots[pos]}
        elif i['type']=='reverse':
            iinstr=i
        elif i['type']=='move':
            iinstr={'type':'move','pos1':i['pos2'],'pos2':i['pos1']}
        
        before=pwrd
        pwrd=funcs[iinstr['type']](pwrd,iinstr)
        print(before+' '+str(i)+' '+pwrd)
        
    return(pwrd)

pwrd='fbgdceah'
#pwrd=retA
def rotaten(pwrd,instr):
    l=len(pwrd)
    n=instr['n']%l
    return(pwrd[n:]+pwrd[:n])

def rotatep(pwrd,instr):
    pos=pwrd.find(instr['let1'])
    if pos>=4:
        pos+=1
    return(rotaten(pwrd,{'n':-1*(pos+1)}))


retB=invert(pwrd,instrs)