f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-03.txt')
contents = f.read()
inp = contents.splitlines()

def common_bit(input,pos,dir): #Find most/least common bit in position pos of all input numbers
    digits=[input[x][pos] for x in range(len(input))]
    if dir=='most':
        if digits.count('1')>=digits.count('0'):
            return('1')
        else:
            return('0')
    elif dir=='least':
        if digits.count('1')<digits.count('0'):
            return('1')
        else:
            return('0')
            
def common_bits(input,dir): #Find most/least common bit in each position and convert resulting number to decimal
    ret=''
    for b in range(len(input[0])):
        ret+=common_bit(input,b,dir)
    print(ret)
    return(int(ret,2)) #Convert to decimal

gamma=common_bits(inp,'most')
epsilon=common_bits(inp,'least')
print(gamma*epsilon)

def bit_filter(input,dir): #For each bit from left to right, find the most/least common and only keep numbers from the list if they match that bit
    i=0 #Starting position
    nums=input.copy()
    while len(nums)>1:
        target=common_bit(nums,i,dir)
        nums=[x for x in nums if x[i]==target]
        i+=1
        
    print(nums[0])
    return(int(nums[0],2))
    
oxygen=bit_filter(inp,'most')
co2=bit_filter(inp,'least')
print(oxygen*co2)
