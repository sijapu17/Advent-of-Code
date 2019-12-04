#Advent of Code 2016 Day 2

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-2.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    
    pos=complex(1,1)
    dirs={'D':1,'R':1j,'U':-1,'L':-1j}
    ret=''
    
    for row in input:
        for i in row:
            pos=pos+dirs[i]
            pos=complex(min(max(pos.real,0),2),min(max(pos.imag,0),2)) #Bound in 0,2
        
        print(pos)
        ret+=str(int(pos.real*3+pos.imag+1))
    return(ret)

#retA=solveA(input)


def solveB(input):
    
    pos=complex(-2,0)
    dirs={'L':-1,'U':1j,'R':1,'D':-1j}
    keys={2j:'1',-1+1j:'2',1j:'3',1+1j:'4',-2:'5',-1:'6',0:'7',1:'8',2:'9',-1-1j:'A',-1j:'B',1-1j:'C',-2j:'D'}
    print(keys[pos])
    ret=''
    
    for row in input:
        for i in row:
            pos1=pos+dirs[i]
            if abs(pos1.real)+abs(pos1.imag)<=2:
                pos=pos1
            print(str(i)+': '+keys[pos])
        
        
        ret+=str(keys[pos])
    return(ret)

retB=solveB(input)