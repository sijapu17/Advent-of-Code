#Advent of Code 2025 Day 2
from functools import cache

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2025/2025-02.txt')
contents = f.read()
input = contents.split(',')

@cache
def find_factors(n): #Compute a set of all factors of n (excluding n itself)
    ret=set()
    if n==1:
        return(ret)
    ret.add(1) #All integers have 1 as a factor, and we don't want to include n as a factor
    sqrt=int(n**0.5) #Upper bound of search is square root of n
    for i in range(2,sqrt+1):
        if n%i==0:
            ret.add(i)
            ret.add(int(n/i))
    return(ret)

def sum_2_repeats(input): #Sum of IDs consisting of 2 repeated strings
    res=0 #Sum of all invalid IDs

    for id_range in input:
        start, end=(int(x) for x in id_range.split('-'))
        for n in range(start,end+1): #Loop through each range in input
            s=str(n)
            l=len(s)
            if l%2==0:
                if s[:int(l/2)]==s[int(l/2):]:
                    res+=n
    return(res)

print(sum_2_repeats(input))

def sum_n_repeats(input): #Sum of IDs consisting of n repeated strings
    res=0 #Sum of all invalid IDs

    for id_range in input:
        start, end=(int(x) for x in id_range.split('-'))
        for n in range(start,end+1): #Loop through each range in input
            s=str(n)
            l=len(s)
            factors=find_factors(l)
            #For each factor of string length, slice ID into length-f sections and see if they are identical
            for f in factors:
                sliced=set([s[x:x+f] for x in range(0,l,f)])
                #If all slices are identical, set will have length 1
                if len(sliced)==1:
                    res+=n
                    break
    return(res)

print(sum_n_repeats(input))