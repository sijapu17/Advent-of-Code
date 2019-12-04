#Advent of Code 2016 Day 7

import re
from collections import Counter
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2016-7.txt')
contents = f.read()
input = contents.splitlines()

def abba(lst):
    for each in lst:
        l=len(each)-3
        if l>0:
            for i in range(l):
                four=each[i:i+4]
                if four[0]!=four[1] and four[0]==four[3] and four[1]==four[2]:
                    return(True)
    return(False)

def solveA(input):
    
    count=0
    for each in input:        
        segments=re.split('\[|\]',each)
        outside=segments[::2]
        inside=segments[1::2]
        if not abba(inside) and abba(outside):
            count+=1
    return(count)

#retA=solveA(input)

def aba(lst):
    abas=[]
    for each in lst:
        l=len(each)-2
        if l>0:
            for i in range(l):
                three=each[i:i+3]
                if three[0]!=three[1] and three[0]==three[2]:
                    abas.append(three)
    return(abas)

def bab(lst,abas):
    if len(abas)>0:
        for aba in abas:
            bab=aba[1]+aba[0]+aba[1]
            for each in lst:
                if bab in each:
                    return(True)                
    return(False)

def solveB(input):
    
    count=0
    for each in input:        
        segments=re.split('\[|\]',each)
        outside=segments[::2]
        inside=segments[1::2]
        abas=aba(outside)
        if bab(inside,abas):
            count+=1
    return(count)

retB=solveB(input)