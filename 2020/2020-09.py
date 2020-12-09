#Advent of Code 2020 Day 9

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-09.txt')
contents = f.read()
input=[int(x) for x in contents.splitlines()]

def check_sums(n,nums): #Check whether any two numbers in nums sum to n
    d=len(nums)
    for i in range(d):
        for j in range(i+1,d):
            if nums[i]+nums[j]==n:
                return(True)
    return(False)

def solveA(input): #Find first position where none of the previous 25 numbers sum to current number
    pos=25
    while pos<=len(input):
        if not check_sums(input[pos],input[pos-25:pos]):
            return(input[pos])
        pos+=1


def solveB(input,target): #Find run of numbers that add to target number
    for i in range(len(input)):
        sum=input[i]
        j=i
        while sum<=target and j+1<len(input):
            if sum==target:
                mn=min(input[i:j+1])
                mx=max(input[i:j+1])
                return(mn+mx)
            j+=1
            sum+=input[j]

target=solveA(input)
print(target)
print(solveB(input,target))