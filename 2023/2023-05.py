#Advent of Code 2023 Day 5
import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-05.txt')
contents = f.read()
input = contents.splitlines()

#Parse input
seeds=[int(x) for x in re.findall(r"\d+",input[0])]
seed_ranges=[(seeds[i],seeds[i+1]) for i in range(0,len(seeds),2)]

#print(seed_ranges)

maps=[]
i=3
current=[] #Current section of maps

while i<len(input):
    if input[i]=='':
        i+=2
        maps.append(current)
        current=[]
    else:
        current.append([int(x) for x in re.findall(r"\d+",input[i])])
        i+=1
maps.append(current)

def find_seed_location(n): #Find location of seed n
    for section in maps:
        for map in section:
            if map[1]<=n<map[1]+map[2]:
                n+=map[0]-map[1]
                break #If mapped once, skip to next section
    return(n)

def find_location_seed(n): #Find seed of location n - may not be needed
    for section in maps[::-1]:
        for map in section:
            if map[0]<=n<map[0]+map[2]:
                n+=map[1]-map[0]
                break #If mapped once, skip to next section
    return(n)

def lowest_location():
    return(min([find_seed_location(x) for x in seeds]))

#print(lowest_location())
def find_best_range(pairs):
    min_loc=float("inf")
    for pair in pairs:
        #print(pair)
        i=0
        while i<pair[1]:
            seed=pair[0]+i
            loc=find_seed_location(seed)
            if loc<min_loc:
                min_loc=loc
                best_seed=seed
                best_pair=pair
            i+=1000000
    print(f'Best Seed {best_seed} --> Loc {min_loc}')
    print(f'Best Pair {best_pair}')
    return(best_pair)

best_pair=find_best_range(seed_ranges)

def best_in_range(range):
    step=int(round((range[1]-range[0])/100)) #Cut range into approx 100 subranges
    if step<1:
        step=1
    min_loc=float("inf")
    i=0  
    seed=0 #Initialise for while loop
    while seed<range[1]:
        seed=range[0]+i
        loc=find_seed_location(seed)
        if loc<min_loc:
            min_loc=loc
            best_seed=seed
        i+=step
    print(f'Range: {range}')
    print(f'Step={step}')
    print(f'Best Seed {best_seed} --> Loc {min_loc}')    
    if step==1: #If step was 1, exact best seed found
        print(f'Global Best Seed {best_seed} --> Global Min Loc {min_loc}')
        return(min_loc)
    else: #Else, best seed is in range below best seed found 
        return((best_seed-step,best_seed))

def binary_search(pair):
    while True:
        pair=best_in_range(pair)
        if type(pair)==int:
            return(pair)

best_range=(best_pair[0],best_pair[0]+best_pair[1]) #Convert from (start,size) to (size,end)

print(binary_search(best_range))