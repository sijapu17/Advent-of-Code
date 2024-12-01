#Advent of Code 2024 Day 1

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-01.txt')
contents = f.read()
input = contents.splitlines()

left=sorted([int(x.split()[0]) for x in input])
right=sorted([int(x.split()[1]) for x in input])

#Part 1 - sum of differences
print(sum([abs(left[i]-right[i]) for i in range(len(left))]))
#Part 2 - similarity scores
print(sum([left[i]*right.count(left[i]) for i in range(len(left))])) 