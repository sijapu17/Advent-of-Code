#Advent of Code 2023 Day 11

from itertools import product

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-11.txt')
contents = f.read()
input = contents.splitlines()

galaxies={}

nonempty_x=set()
nonempty_y=set()

def populate_galaxies(): #Positions of galaxies before expansion
    n=1 #Galaxy number
    for j in range(len(input)):
        for i in range(len(input[j])):
            if input[j][i]=='#':
                galaxies[n]=complex(i,j)
                nonempty_x.add(i)
                nonempty_y.add(j)
                n+=1

populate_galaxies()

def paired_distances(map:dict,ex): #Sum all pairwise distances between galaxies, adding ex rows/cols to each empty row/col 
    sum=0
    for g0, g1 in product(map.values(),map.values()):
        x0=int(min(g0.real,g1.real))
        x1=int(max(g0.real,g1.real))
        y0=int(min(g0.imag,g1.imag))
        y1=int(max(g0.imag,g1.imag))
        expanse_x=len(set(range(x0,x1+1))-nonempty_x) #Number of columns to expand
        expanse_y=len(set(range(y0,y1+1))-nonempty_y) #Number of rows to expand
        sum+=int(abs(g0.real-g1.real)+abs(g0.imag-g1.imag))+(ex-1)*(expanse_x+expanse_y)
    return(int(sum/2))

print(paired_distances(galaxies,2))
print(paired_distances(galaxies,1000000))