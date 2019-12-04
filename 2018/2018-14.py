#Advent of Code 2018 Day 14

input='306281'

def solveA(input):
    recipes=[3,7] #Starting recipes
    i=[0,1] #Pointers for each elf's current position
    while len(recipes)<input+10:
        r=[recipes[i[0]],recipes[i[1]]]
        new=sum(r)
        if new<10:
            recipes.append(new)
        else:
            recipes.append(1)
            recipes.append(new-10)
        move=[] #Distance for each pointer to move
        for x in range(len(i)):
            move.append((r[x]+1))
        i=[sum(x)%len(recipes) for x in zip(i, move)]
    #print(recipes)
    ret=''.join(str(y) for y in recipes[input:input+10])
    return(ret)
        
#input=5
#retA=solveA(input)
        
def solveB(input):
    recipes=[3,7] #Starting recipes
    i=[0,1] #Pointers for each elf's current position
    toMatch=[int(d) for d in input]
    end=0 #Index of last recipe before matched set
    j=0 #Index of which digit in input to match next
    while True:
        r=[recipes[i[0]],recipes[i[1]]]
        new=sum(r)
        if new<10:
            recipes.append(new)
            added=[new]
        else:
            recipes.append(1)
            recipes.append(new-10)
            added=[1,new-10]
        for k in added:
            if k==toMatch[j]:
                if j==0:
                    end=len(recipes)-1
                j+=1
                if j>=len(toMatch):
                    return(end)
            else:
                if k==toMatch[0]:
                    end=len(recipes)-1
                    j=1
                else:
                    j=0
        move=[] #Distance for each pointer to move
        for x in range(len(i)):
            move.append((r[x]+1))
        i=[sum(x)%len(recipes) for x in zip(i, move)]


input='306281'
retB=solveB(input)