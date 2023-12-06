#Advent of Code 2023 Day 6
import re
import math

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-06.txt')
contents = f.read()
input = contents.splitlines()

#Part 1 times and records
times=[int(x) for x in re.findall(r"\d+",input[0])]
records=[int(x) for x in re.findall(r"\d+",input[1])]
#Part 2 time and record
time2=int(re.findall(r"\d+",input[0].replace(" ",""))[0])
record2=int(re.findall(r"\d+",input[1].replace(" ",""))[0])

# d = Distance travelled
# t = Race time
# x = time button is held down for
# d=x(t-x) = -x^2 +tx
# x^2 - tx + d = 0

def count_winning_possibilities(time,record):
    t=time
    d=record+0.00001 #Add small amount to record so ties are not counted
    root1=(t-math.sqrt(t**2-4*d))/2 #Quadratic formula roots
    root2=(t+math.sqrt(t**2-4*d))/2    
    return(math.floor(root2)-math.ceil(root1)+1)

print(math.prod([count_winning_possibilities(times[i],records[i]) for i in range(len(times))]))

print(count_winning_possibilities(time2,record2))