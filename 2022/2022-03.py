#Advent of Code 2022 Day 3

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-03.txt')
contents = f.read()
input = contents.splitlines()

def priority(x:str): #Return priority value of given character, based on a-z=1-26, A-Z=27-52
    if x.isupper():
        p=ord(x)-38
    else:
        p=ord(x)-96
    #print(p)
    return(p)

def find_overlap(rucksack:str): #Return character which appears in both halves of rucksack
    half=int(len(rucksack)/2)
    for c in rucksack[:half]:
        if c in rucksack[half:]:
            #print(c)
            return(c)
   
def find_badge(r0,r1,r2): #Return character which appears in all three rucksacks
    for c in r0:
        if c in r1:
            if c in r2:
                return(c)

def score_overlaps(input): #Loop through all rucksacks and sum total score
    total=0
    for x in input:
        total+=priority(find_overlap(x))
    return(total)
       
def score_badges(input): #Loop through all rucksack trios and sum total score
    total=0
    for i in range(0,len(input),3):
        total+=priority(find_badge(input[i],input[i+1],input[i+2]))
    return(total)

print(score_overlaps(input))
print(score_badges(input))