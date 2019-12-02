#Advent of Code 2015 Day 12

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-12.txt')
contents = f.read()
input=eval(contents)

num='-0123456789'

def nCount(input):
    sum=0
    current=''
    for c in input:
        if c in num:
            current+=c
        elif len(current)>0:
            sum+=int(current)
            current=''
    return(sum)

#retA=solveA(input)

def solveB(input):
    total=0
    stack=input[:] #Components to be checked
    while len(stack)>0:
        part=stack.pop()
        if type(part)==list: #Add each list member to stack to be checked
            for p in part:
                stack.append(p)
        elif type(part)==str: #Extract numbers from strings as in part a
            total+=nCount(part)
        elif type(part)==int: #Add integers directly to total
            total+=part
        elif type(part)==dict: #Check dict values for word "red"
            if "red" not in part.values():
                for p in part.values(): #If red not found, add each value to stack to be checked
                    stack.append(p)
        else:
            print('Type '+str(type(part))+' not recognised')
    return(total)
                  
retB=solveB(input)
                
                