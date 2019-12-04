#Advent of Code 2016 Day 18

input='...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^.....^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^'

def isSafe(behind): #Checks whether tile is safe, based on three tiles behind it
    if behind[0]!=behind[2]:
        return(False)
    return(True)

def getBehind(row,pos): #Find three tiles behind given tile
    r='.'+row+'.' #Add safe spots onto each side
    return(r[pos:pos+3])
    
def solveA(input,nRows):
    width=len(input)
    room=[input]
    sCount=input.count('.')
    for i in range(nRows-1):
        if i%4000==1:
            print('Step '+str(i))
        newRow=''
        oldRow=room[-1]
        for j in range(width):
            if isSafe(getBehind(oldRow,j)):
                newRow+='.'
                sCount+=1
            else:
                newRow+='^'
        room.append(newRow)
    return(sCount)
        
retA=solveA(input,40)
retB=solveA(input,400000)