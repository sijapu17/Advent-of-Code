#Advent of Code 2022 Day 6

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-06.txt')
input = f.read()

def find_unique(size): #Find position of first unique string of given size
    for i in range(len(input)):
        s=set(input[i:i+size])
        if len(s)==size:
            return(i+size)

print(find_unique(4))
print(find_unique(14))