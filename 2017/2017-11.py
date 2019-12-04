#Advent of Code 2017 Day 11

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-11.txt')
contents = f.read()
input = contents.split(",")

def CountDirs(input):
    dir={}
    dir['ne']=0
    dir['n']=0
    dir['nw']=0
    for d in input:
        if d=='ne':
            dir['ne']+=1
        elif d=='sw':
            dir['ne']-=1
        elif d=='n':
            dir['n']+=1
        elif d=='s':
            dir['n']-=1
        elif d=='nw':
            dir['nw']+=1
        elif d=='se':
            dir['nw']-=1
        else:
            print('Warning: direction '+d+' not recognised')
    return(dir)

dirs=CountDirs(input)
#dirs2=CountDirs(input[:5103])
#test={'ne':4,'n':-10,'nw':5}

def PathDist(input): #Shortest path length of grid point
    in1=input.copy()
    simple=0 #Condition to break out of loop
    while simple==0:
        while(in1['nw']>0 and in1['ne']>0):
            in1['nw']-=1
            in1['ne']-=1
            in1['n']+=1 #Combine 1 step NW plus 1 step NE to 1 step N
        while(in1['nw']<0 and in1['ne']<0):
            in1['nw']+=1
            in1['ne']+=1
            in1['n']-=1 #Combine 1 step SE plus 1 step SW to 1 step S
        while(in1['ne']>0 and in1['n']<0):
            in1['ne']-=1
            in1['n']+=1
            in1['nw']-=1 #Combine 1 step NE plus 1 step S to 1 step SE
        while(in1['ne']<0 and in1['n']>0):
            in1['ne']+=1
            in1['n']-=1
            in1['nw']+=1 #Combine 1 step SW plus 1 step N to 1 step NW       
        while(in1['nw']>0 and in1['n']<0):
            in1['nw']-=1
            in1['n']+=1
            in1['ne']-=1 #Combine 1 step NW plus 1 step S to 1 step SW          
        while(in1['nw']<0 and in1['n']>0):
            in1['nw']+=1
            in1['n']-=1
            in1['ne']+=1 #Combine 1 step SE plus 1 step N to 1 step NE    
        if ((in1['n']==0 and in1['nw']*in1['ne']<=0) or
            (in1['nw']==0 and in1['nw']*in1['ne']>=0) or
            (in1['ne']==0 and in1['nw']*in1['ne']>=0)):
            simple=1
    #print(str(in1)) #Should be up to 2 directions next to each other
    ln=abs(in1['nw'])+abs(in1['n'])+abs(in1['ne'])
    return(ln)

retA=PathDist(dirs)
#testA=PathDist(dirs2)

def Furthest(input): #Calculate furthest distance away from origin during the walk
    i=len(input)
    mx=0 #Max distance found
    while (i>mx):
        in1=input[:i-1]
        dirs=CountDirs(in1)
        ln=PathDist(dirs)
        mx=max(mx,ln) #Reassign mx is new path is larger than current max
        if (i%100==0):
            print('Step '+str(i)+': '+str(ln)+' steps')
        i-=1
    return(mx)

retB=Furthest(input)