#Advent of Code 2017 Day 14

#input='flqrgnkx'
input='ugkiagan'

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

#ascii1=list2ASCII(input)

def sparseHash(lengths):
    param={}
    param['knot']=list(range(256)) #Initial knot
    param['pos']=0 #Initial position
    param['skp']=0 #Initial skip size
    for i in range(64):
        param=knotIterate(param['knot'],lengths,param['pos'],param['skp'])
    return(param['knot'])

#sparse=sparseHash(ascii1)
#stest=sparseHash(input)

def denseHash(sparse):
    dense=[]
    for i in range(16):
        dense.append((sparse[16*i]^sparse[16*i+1]^sparse[16*i+2]^sparse[16*i+3]
                  ^sparse[16*i+4]^sparse[16*i+5]^sparse[16*i+6]^sparse[16*i+7]
                  ^sparse[16*i+8]^sparse[16*i+9]^sparse[16*i+10]^sparse[16*i+11]        
                  ^sparse[16*i+12]^sparse[16*i+13]^sparse[16*i+14]^sparse[16*i+15]))
    return(dense)
                  
#dense=denseHash(sparse)

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

def binRep(hx): #Binary representation of hexadecimal
    bn=''
    i=0
    for n in hx:
        binn=bin(int(n, 16))[2:].zfill(4)
        bn+=binn
        i+=1
    return(bn)

#hexstr=hexRep(dense)
#bn=binRep('f')

def knotHash(input):    
    ascii1=list2ASCII(input)
    sparse=sparseHash(ascii1)    
    dense=denseHash(sparse)
    hexstr=hexRep(dense)
    return(hexstr)
    
def solveA(input):
    rows=[] #This will store the 128 rows
    sum=0
    for i in range(128):
        hashin=input+'-'+str(i)
        hashout=knotHash(hashin)
        hashbin=binRep(hashout)
        sum+=hashbin.count('1')
        rows.append(hashbin)
    return(sum)

#retA=solveA(input)

def createGrid(input):
    rows=[] #This will store the 128 rows
    for i in range(128):
        hashin=input+'-'+str(i)
        hashout=knotHash(hashin)
        hashbin=binRep(hashout)
        r=[]
        for i in range(len(hashbin)):
            r.append(int(hashbin[i]))
        rows.append(r)
    return(rows)

grid=createGrid(input)

def coords(dim): #Create list of coords in the dim*dim grid
    clist=[]
    for i in range(dim):
        for j in range(dim):
            clist.append((i,j))
    return clist

def checkGroup(grid,c0,dim): #Find all other coords in the group
    toCheck=[c0]
    while len(toCheck)>0:
        c=toCheck.pop()
        if c[0]>0 and grid[c[0]-1][c[1]]==1: #Check cell to left
            toCheck.append((c[0]-1,c[1]))
        if c[0]<dim-1 and grid[c[0]+1][c[1]]==1: #Check cell to right
            toCheck.append((c[0]+1,c[1]))
        if c[1]>0 and grid[c[0]][c[1]-1]==1: #Check cell below
            toCheck.append((c[0],c[1]-1))
        if c[1]<dim-1 and grid[c[0]][c[1]+1]==1: #Check cell above
            toCheck.append((c[0],c[1]+1))
        grid[c[0]][c[1]]=0 #Set to zero once checked

#grid=[[1,0,1],[0,1,1],[1,0,1]]

def solveB(grid): #Count number of distinct groups in grid
    dim=len(grid)
    clist=coords(dim)
    ngroups=0
    for c in clist:
        if grid[c[0]][c[1]]==1:
            checkGroup(grid,c,dim)
            ngroups+=1
    return(ngroups)

retB=solveB(grid)
    