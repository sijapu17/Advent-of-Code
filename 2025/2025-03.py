#Advent of Code 2025 Day 3

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-03.txt')
contents = f.read()
input = contents.splitlines()

def sum_largest_2_joltages(input): #Find largest 2-digit number in each line of input, and sum
    sum=0
    for bank in input:
        joltage=''
        joltage+=max(bank[:-1])
        joltage+=max(bank[bank.find(joltage[-1])+1:])
        sum+=int(joltage)
    return(sum)

#print(sum_largest_2_joltages(input))

def sum_largest_n_joltages(input,n): #Find largest n-digit number in each line of input, and sum
    sum=0
    for bank in input:
        digit=n
        joltage=max(bank[:-1*(digit-1)])
        digit-=1
        start=0
        while digit>0:
            #Start bound of max search is one digit after the previously-used digit 
            start=bank.find(joltage[-1],start)+1
            #End bound of max search far enough from end of bank to avoid running out of batteries before end of search
            if digit==1:
                end=None
            else:
                end=-1*(digit-1)
            joltage+=max(bank[start:end])
            digit-=1
        #print(joltage)
        sum+=int(joltage)

    return(sum)

print(sum_largest_n_joltages(input,2)) #Part 1
print(sum_largest_n_joltages(input,12)) #Part 2