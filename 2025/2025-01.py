#Advent of Code 2025 Day 1

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-01.txt')
contents = f.read()
input = contents.splitlines()

zeroes_1=0 #Count how many times 0 is reached at end of move
zeroes_2=0 #Count how many times 0 is reached at any time
dial_pos=50 #Dial position (0-99)

for inst in input:
    magnitude=int(inst[1:])
    if inst[0]=='L': #Negative turn
        for i in range(magnitude):
            dial_pos-=1
            if dial_pos==0:
                zeroes_2+=1
            elif dial_pos<0:
                dial_pos+=100
    elif inst[0]=='R': #Positive turn
        for i in range(magnitude):
            dial_pos+=1
            if dial_pos==100:
                zeroes_2+=1
                dial_pos-=100
    
    if dial_pos==0:
        zeroes_1+=1

print(zeroes_1)
print(zeroes_2)