#Advent of Code 2025 Day 6

from functools import reduce

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-06.txt')
contents = f.read()

input1 = [x.split() for x in contents.splitlines()] #Part 1
input2 = contents.splitlines() #Part 2

def add(a,b):
    return(a+b)

def mult(a,b):
    return(a*b)

ops={'+':add,'*':mult}
identity={'+':0,'*':1}

#Part 1

problems=[[] for x in range(len(input1[0]))] #Create empty list for each problem

#Add each number to its problem list
for j in range(len(input1)-1):
    for i in range(len(problems)):
        problems[i].append(int(input1[j][i]))

#Grand total
grand_total1=0

#For each problem, sum or multiply according to final row
for i in range(len(problems)):
    grand_total1+=reduce(ops[input1[-1][i]], problems[i])   

print(grand_total1)
                           
#Part 2 - parse vertically
grand_total2=0
current_problem=0

for i in range(len(input2[0])):
    #If column contains an op, start new problem
    if input2[-1][i] in ('+','*'):
        grand_total2+=current_problem
        current_op=input2[-1][i]
        current_problem=identity[current_op]
    #Add/mult number in column to current_problem
    current_number=''.join([input2[x][i] for x in range(len(input2)-1)])
    if len(str.strip(current_number))>0:
        current_problem=ops[current_op](current_problem,int(current_number))

grand_total2+=current_problem #Add final problem result
print(grand_total2)