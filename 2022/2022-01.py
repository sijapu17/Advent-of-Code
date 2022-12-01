#Advent of Code 2022 Day 1

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-01.txt')
contents = f.read()
input = contents.splitlines()

def count_calories(input): #Consolidate list of item calories into sorted elf calorie totals
    elf_totals=[]
    current=0
    for x in input:
        if len(x)==0:
            elf_totals.append(current)
            current=0
        else:
            current+=int(x)
    return(sorted(elf_totals))

totals=count_calories(input)
print(totals[-1]) #Part 1
print(sum(totals[-3:])) #Part 2