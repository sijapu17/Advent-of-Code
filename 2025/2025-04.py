#Advent of Code 2025 Day 4

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-04.txt')
contents = f.read()
input = contents.splitlines()

rolls=set()
x_max=len(input[0])
y_max=len(input)

#Import map
for j in range(y_max):
    for i in range(x_max):
        if input[j][i]=='@':
            rolls.add(complex(i,j))

def nAdjacent(pos,rolls):
    count=0
    for i in (-1,0,1):
        for j in (-1j,0,1j):
            if i!=0 or j!=0: #Avoid counting self as neighbour
                nPos=pos+i+j
                if nPos in rolls:
                    count+=1
    return(count)
    
print(sum([x<4 for x in [nAdjacent(c,rolls) for c in rolls]]))

def print_map(rolls):
    ret=''
    for j in range(y_max):
        for i in range(x_max):
            if complex(i,j) in rolls:
                ret+='@'
            else:
                ret+='.'
        ret+='\n'
    print(ret)

def remove_rolls(rolls): #Iteratively remove rolls until no more rolls can be removed
    old_rolls=rolls.copy()
    orig_tot=len(old_rolls) #Number of rolls at start
    while True:
        new_rolls=set()
        #Rolls that cannot be removed are added to new_rolls
        for r in old_rolls:
            if nAdjacent(r,old_rolls)>=4:
                new_rolls.add(r)
        #print_map(new_rolls)
        if len(new_rolls)==len(old_rolls):
            #Final count of rolls that have been removed
            return(orig_tot-len(new_rolls))
        old_rolls=new_rolls

print(remove_rolls(rolls))