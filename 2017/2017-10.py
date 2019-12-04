#Advent of Code 2017 Day 10

input=(192,69,168,160,78,1,166,28,0,83,198,2,254,255,41,12)
#input=(1,2,3)

def solveA(input):
    knot=list(range(256))
#    knot=list(range(5))
    pos=0 #Current position
    ln=len(knot)
    for i in range(len(input)):
        #print('Skip size='+str(i))
        #print('Pos='+str(pos))
        overflow=max(pos+input[i]-ln,0) #Check whether section to flip loops back to beginning
        if overflow==0:
            toFlip=knot[pos:pos+input[i]] #Substring to flip
        else:
            toFlip=knot[pos:]+knot[:overflow]
        #print(str(toFlip))
        toFlip.reverse()
        #print(str(toFlip))
        if overflow==0:
            knot=knot[:pos]+toFlip+knot[pos+input[i]:]
        else:
            knot=toFlip[-overflow:]+knot[overflow:pos]+toFlip[:-overflow]
        pos=(pos+input[i]+i)%ln #Increase position by length plus skip size (which increases by 1 each step)
        #print('Knot: '+str(knot))
        ret=knot

    return(ret)
    
#retA=solveA(input)

def knotIterate(knot,lengths,pos,skp):
    kln=len(knot)
    for i in range(len(lengths)):
        #print('Skip size='+str(i))
        #print('Pos='+str(pos))
        #skp=skp%kln
        overflow=max(pos+lengths[i]-kln,0) #Check whether section to flip loops back to beginning
        if overflow==0:
            toFlip=knot[pos:pos+lengths[i]] #Substring to flip
        else:
            toFlip=knot[pos:]+knot[:overflow]
        #print(str(toFlip))
        toFlip.reverse()
        #print(str(toFlip))
        if overflow==0:
            knot=knot[:pos]+toFlip+knot[pos+lengths[i]:]
        else:
            knot=toFlip[-overflow:]+knot[overflow:pos]+toFlip[:-overflow]
        pos=(pos+lengths[i]+skp)%kln #Increase position by length plus skip size (which increases by 1 each step)
        skp+=1
    ret={}
    ret['knot']=knot
    ret['pos']=pos
    ret['skp']=skp
    return(ret)

def list2ASCII(input):
    suffix=[17, 31, 73, 47, 23] #standard length ascii suffix
    instr=str(input)
    instr1=''.join( c for c in instr if  c not in '() ' ) #Remove brackets
    ascii=[ord(c) for c in instr1]
    return(ascii+suffix)

ascii1=list2ASCII(input)

def sparseHash(lengths):
    param={}
    param['knot']=list(range(256)) #Initial knot
    param['pos']=0 #Initial position
    param['skp']=0 #Initial skip size
    for i in range(64):
        param=knotIterate(param['knot'],lengths,param['pos'],param['skp'])
    return(param['knot'])

sparse=sparseHash(ascii1)
#stest=sparseHash(input)

def denseHash(sparse):
    dense=[]
    for i in range(16):
        dense.append((sparse[16*i]^sparse[16*i+1]^sparse[16*i+2]^sparse[16*i+3]
                  ^sparse[16*i+4]^sparse[16*i+5]^sparse[16*i+6]^sparse[16*i+7]
                  ^sparse[16*i+8]^sparse[16*i+9]^sparse[16*i+10]^sparse[16*i+11]        
                  ^sparse[16*i+12]^sparse[16*i+13]^sparse[16*i+14]^sparse[16*i+15]))
    return(dense)
                  
dense=denseHash(sparse)

def hexRep(dense): #Hexadecimal representation
    hx=''
    i=0
    for n in dense:
        #print('i='+str(i))
        #print('n='+str(n))
        hxn="0x{:02x}".format(n)[2:]
        #print ('hexn='+str(hxn))
        hx+=hxn
        i+=1
    return(hx)

hexstr=hexRep(dense)