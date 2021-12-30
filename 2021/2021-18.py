#Advent of Code 2021 Day 18

import math
from functools import reduce
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-18.txt')
contents = f.read()
inp = contents.splitlines()

def listify(s:str): #Turn input string into a list of integers and punctuation
    ret=[] #List to return
    num='' #String for temporarily storing digits
    for c in s:
        if c.isnumeric():
            num+=c
        else:
            if len(num)>0: #Append any digits found as an integer
                ret.append(int(num))
                num=''
            ret.append(c)
    return(ret)

def stringify(l:list): #Turn list back into string for printing
    ret=''
    for x in l:
        if type(x) is int:
            ret+=str(x)
        else:
            ret+=x
    return(ret)

def explode(num:list): #Explode snailfish number if a pair is nested within 4 pairs
    p=0 #Pointer
    level=0
    while p<len(num):
        if level>4 and type(num[p]) is int: #Explosion criteria
            l=num[p] #Left number
            r=num[p+2] #Right number
            #Look left to find the next int (if it exists) and add l to it
            pl=p-3
            while pl>=0: 
                if type(num[pl]) is int:
                    num[pl]+=l
                    break
                pl-=1
            #Look right to find the next int (if it exists) and add r to it
            pr=p+3
            while pr<=len(num)-1: 
                if type(num[pr]) is int:
                    num[pr]+=r
                    break
                pr+=1
            #Replace exploded pair with 0
            num[p-1]=0
            for n in range(4):
                del num[p]
            return(True) #Indicate that explosion has occurred
        else:
            if num[p]=='[':
                level+=1
            elif num[p]==']':
                level-=1
            p+=1
    return(False) #Indicate no explosion occurred

def split(num:list): #Split snailfish number if it is at least 10
    for p in range(len(num)):
        if type(num[p]) is int and num[p]>9:
            l=int(math.floor(num[p]/2))
            r=int(math.ceil(num[p]/2))
            num[p:p+1]=['[',l,',',r,']']
            return(True) #Indicate that split has occurred
    return(False) #Indicate no split occurred

def add(a:list,b:list): #Add two numbers together into a new number pair and then process the result
    added=['[']+a[:]+[',']+b[:]+[']']
    return(process_number(added))

def process_number(num:list): #Perform explosions and splits until no more are possible
    while True:
        if not explode(num):
            if not split(num):
                return(num)

def add_list(inp): #Sequentially add each number in input list
    l=[listify(x) for x in inp] #Listify each line in input so it can be processed
    return(reduce(add,l))

def magnitude(num:list): #Calculate magnitude of reduced sum
    if len(num)==1:
        return(num[0])
    p=0 #Pointer
    level=0
    #Find top-level comma
    for p in range(len(num)):
        x=num[p]
        if level==1 and x==',':
            comma=p
            break
        else:
            if x=='[':
                level+=1
            elif x==']':
                level-=1
            p+=1
    #Split num into [a,b] pair
    a=num[1:p]
    b=num[p+1:-1]
    return(3*magnitude(a)+2*magnitude(b))

def max_pair(inp): #Find max possible magnitude from adding two numbers
    l=[listify(x) for x in inp] #Listify each line in input so it can be processed
    mx=0
    for a in range(len(l)):
        for b in range(len(l)):
            if a!=b:
                mx=max(mx,magnitude(add(l[a],l[b])))
                mx=max(mx,magnitude(add(l[b],l[a])))
    return(mx)

print(magnitude(add_list(inp))) #Sum of all lines
print(max_pair(inp)) #Max sum of two lines