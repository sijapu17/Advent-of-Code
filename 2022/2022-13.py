#Advent of Code 2022 Day 13
import ast
from functools import total_ordering

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-13.txt')
contents = f.read()
inp = contents.splitlines()

@total_ordering
class Packet():
    def __init__(self,s) -> None:
        self.data=ast.literal_eval(s)

    def __eq__(self,other) -> bool:
        return(self.data==other.data)
    
    def __lt__(self,other) -> bool:
        return(compare(self.data,other.data))
    
    def __str__(self) -> str:
        return('P'+str(self.data))
    
    def __repr__(self) -> str:
        return('P'+str(self.data))
    

def import_pairs(inp): #Import packets in pairs for part 1
    pairs=[]
    i=0
    while i<len(inp):
        p=[]
        p.append(Packet(inp[i]))
        p.append(Packet(inp[i+1]))
        pairs.append(p)
        i+=3
    return(pairs)

def import_list(inp): #Import packets in full list for part 2
    list=[]
    for line in inp:
        if len(line)>0:
            list.append(Packet(line))
    #Add in divider packets
    list.append(Packet('[[2]]'))
    list.append(Packet('[[6]]'))
    return(list)

def compare(a,b): #Return True if a<b according to rules, False if a>b
    #print(f'Compare {a} vs {b}')
    if type(a)==int and type(b)==int:
        if a==b:
            return('Equal')
        return(a<b)
    elif type(a)==int and type(b)==list:
        return(compare([a],b))
    elif type(a)==list and type(b)==int:
        return(compare(a,[b]))
    elif type(a)==list and type(b)==list:
        i=0
        while i<min(len(a),len(b)):
            ret=(compare(a[i],b[i]))
            if type(ret)==bool:
                return(ret)
            i+=1
        if len(a)==len(b):
            return('Equal')
        return(len(a)<len(b))

def count_ordered(pairs): #Count number of pairs in correct order
    count=0
    index=0
    for p in pairs:
        index+=1
        count+=(index*(p[0]<p[1]))
    return(count)

def divider_indices(lst): #Sort list of packets, find indices of divider packets
    std=lst[:]
    std.sort()
    print(std)
    p2=std.index(Packet('[[2]]'))+1
    p6=std.index(Packet('[[6]]'))+1
    return(p2*p6)

#pairs=import_pairs(inp)
#print(count_ordered(pairs))

lst=import_list(inp)
print(divider_indices(lst))

#print(Packet('[[2]]')<Packet('[[6]]'))
#print(sorted([Packet('[[6]]'),Packet('[[2]]')]))