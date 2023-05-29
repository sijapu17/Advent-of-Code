#Advent of Code 2022 Day 20

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-20.txt')
contents = f.read()
inp = contents.splitlines()

def create_file():
    return([int(x) for x in inp])

def mix(file,n,key): #Mix file n times, according to mixing rules
    pairs=[] #List of original positions matched up with their values
    for i in range(len(file)):
        pairs.append((i,key*file[i]))
    pairs0=pairs.copy() #Copy of starting state for indexing
    #Perform mix n times
    for x in range(n):
        for i in range(len(file)):
            pos=pairs.index(pairs0[i])
            to_move=pairs.pop(pos)
            newpos=(pos+to_move[1])%len(pairs)
            pairs.insert(newpos,to_move)
    return([x[1] for x in pairs])

def sum_indices(file): #Return sum of 1000, 2000, 3000 after value 0
    zeropos=file.index(0)
    return(file[(zeropos+1000)%len(file)]+file[(zeropos+2000)%len(file)]+file[(zeropos+3000)%len(file)])

#Part 1
file=create_file()
file=mix(file,1,1)
print(sum_indices(file))
#Part 2
file=create_file()
file=mix(file,10,811589153)
print(sum_indices(file))
