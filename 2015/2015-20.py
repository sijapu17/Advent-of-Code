#Advent of Code 2015 Day 20
import math
from collections import defaultdict

target=33100000
#target=100

def getFactors(n): #Return list of factors of n
    factors=[]
    for i in range(1,math.ceil(n/2)+1):
        if n%i==0:
            factors.append(i)
    ret=factors+[n]
    return(ret)

#def solveA(target):
#    i=3
#    maxPresents=0
#    while True:
#        factors=getFactors(i)
#        presents=10*sum(factors)
#        if presents>=target:
#            return(i)
#        if presents>maxPresents:
#            print(str(i)+': '+str(presents))
#            maxPresents=presents
#        i+=1
        
def solveA(target):
    house=defaultdict(int)
    for i in range(1,int(target/10)):
        if i%(target/1000)==1:
            print(i)
        for j in range(0,int(target/10),i):
            house[j]+=i*10
    del house[0]
    for h in sorted(house): #Find lowest numbered house with over target number of presents
        if house[h]>=target:
            print(h)
            return(house)
            
retA=solveA(target)
ho=retA[0]