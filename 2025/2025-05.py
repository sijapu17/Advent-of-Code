#Advent of Code 2025 Day 5

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-05.txt')
contents = f.read()
input = contents.splitlines()

#Create ranges and ingredient IDs
ranges=[]
IDs=set()
for line in input:
    if '-' in line:
        ranges.append(tuple([int(x) for x in line.split('-')]))
    elif line!='':
        IDs.add(int(line))
#Sort ranges by first element, for part 2
ranges.sort(key=lambda x : x[0])

#Count how many IDs are in a fresh range
fresh=0
for i in IDs:
    for r in ranges:
        if r[0]<=i<=r[1]:
            fresh+=1
            break

print(fresh)

#Count total possible fresh items across all ranges
fresh_total=0 #Count of fresh items
pointer=0 #Track of which IDs have been reached so far

for r in ranges:
    if pointer<r[0]: #If current range is fully above pointer, count whole range
        fresh_total+=r[1]-r[0]+1
        pointer=r[1]
    elif r[0]<=pointer<r[1]: #If pointer intersects current range, count range above pointer
        fresh_total+=r[1]-pointer
        pointer=r[1]
    else: #If pointer is above current range, nothing left to count
        pass
    #print(f'{range}')

print(fresh_total)
#2550280714933 too low
