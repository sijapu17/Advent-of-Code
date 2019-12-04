#Advent of Code 2018 Day 11
import math
serial=6042

def makeGrid(serial):
    grid={}
    for j in range(1,302):
        for i in range(1,302):
            power=((((i+10)*j)+serial)*(i+10))
            power=math.floor(power/100%10)-5
            grid[complex(i,j)]=power
    return(grid)


def getPower(grid,i,j): #Returns power of battery at coord, or 0 if coord is out of bounds
    if i<1 or j<1:
        return(0)
    else:
        return(grid[complex(i,j)])

def makeSumGrid(grid): #For each coord, sum all coords above and to the left
    sGrid={}
    for j in range(1,302):
        for i in range(1,302):
            sGrid[complex(i,j)]=getPower(grid,i,j)+getPower(sGrid,i,j-1)+getPower(sGrid,i-1,j)-getPower(sGrid,i-1,j-1)
    print('sGrid complete')
    return(sGrid)

def solveA(serial):
    grid=makeGrid(serial)
    maxPower=-1000
    maxCoord=None
    for j in range(1,299):
        for i in range(1,299):
            power=0
            for b in range(3):
                for a in range(3):
                    power+=grid[complex(i+a,j+b)]
            if power>maxPower:
                maxPower=power
                maxCoord='('+str(i)+','+str(j)+')'
    return(maxCoord)

#retA=solveA(grid)
grid=makeGrid(serial)
sGrid=makeSumGrid(grid)
    
def displayGrid(grid,x,y):
    ret=''
    for j in range(1,y+1):
        for i in range(1,x+1):
            power=str(getPower(grid,i,j))
            pad=max(0,5-len(power))
            ret+=power
            ret+=' '*pad
            
        ret+='\n'
    print(ret)    
    
displayGrid(grid,23,108)
displayGrid(sGrid,23,108)

def squarePower(sGrid,i,j,s):
    power=getPower(sGrid,i,j)+getPower(sGrid,i-s,j-s)-getPower(sGrid,i-s,j)-getPower(sGrid,i,j-s)
    return(power)

def solveB(serial):
    grid=makeGrid(serial)
    sGrid=makeSumGrid(grid)
    maxPower=-1000
    maxCoord=None
    for s in range(1,301):
        maxSizePower=-1000
        for j in range(1,302-s):
            for i in range(1,302):
                power=squarePower(sGrid,i,j,s)
                if power>maxSizePower:
                    maxSizePower=power
                    if power>maxPower:
                        maxPower=power
                        maxCoord=str(i-s+1)+','+str(j-s+1)+','+str(s)
                        print(maxCoord+': '+str(power))
        print('s='+str(s)+' max power: '+str(maxSizePower))
    return(maxCoord)
#232,251,12
retB=solveB(serial)
#Incorrect 242,1,5