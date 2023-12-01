#Advent of Code 2023 Day 1

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-01.txt')
contents = f.read()
input = contents.splitlines()

#Find first and last digit in each row, combining into a 2-digit number
def getFirstLast(input):
    ret=0
    for row in input:
        digits=[int(x) for x in row if x.isdigit()]
        ret+=digits[0]*10+digits[-1]
    return(ret)

words={'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9} #Valid spelled out digits

#Find first digit or spelled-out word in string
def scanRowFirst(row):
    for i in range(len(row)):
        if row[i].isdigit():
            return(int(row[i]))
        else:
            for w,v in words.items():
                if w in row[:i+1]:
                    return(v)
#Find last digit or spelled-out word in string
def scanRowLast(row : str):
    for i in range(len(row)-1,-1,-1):
        if row[i].isdigit():
            return(int(row[i]))
        else:
            for w,v in words.items():
                if w in row[i:]:
                    return(v)

#Find first and last digit (or spelled-out word) in each row, combining into a 2-digit number        
def getFirstLastWord(input):
    ret=0
    for row in input:
        ret+=scanRowFirst(row)*10+scanRowLast(row)
    return(ret)

print(getFirstLast(input)) #Part 1
print(getFirstLastWord(input)) #Part 2