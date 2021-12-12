#Advent of Code 2021 Day 8
import functools
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-08.txt')
contents = f.read()
inp = contents.splitlines()

def count1478(inp): #Count all occurrences of digits 1,4,7,8 based on length
    ret=0
    outs=[x.split(' | ')[1].split() for x in inp]
    for l in outs:
        for o in l:
            if len(o) in (2, 3, 4, 7):
                ret+=1
    print(ret)

def decode_all(inp): #Decode each line
    sum=0
    for line in inp:
        key=decode_signal(line.split(' | ')[0].split())
        value=''
        for digit in line.split(' | ')[1].split():
            value+=str(key[frozenset(digit)])
        sum+=int(value)
    return(sum)
        

def decode_signal(encoded): #Take one list of encoded 0-9 signals and create a key to decode them
    key={}
    # 1: (CF) [len2]
    one=frozenset([x for x in encoded if len(x)==2][0])
    key[1]=one
    key[one]=1
    # 7: (ACF) [len3]
    seven=frozenset([x for x in encoded if len(x)==3][0])
    key[7]=seven
    key[seven]=7
    # A: 7 - 1
    A=seven-one
    key['A']=A
    # 4: BCDF [len4]
    four=frozenset([x for x in encoded if len(x)==4][0])
    key[4]=four
    key[four]=4
    # 8: ABCDEFG [len7]
    eight=frozenset([x for x in encoded if len(x)==7][0])
    key[8]=eight
    key[eight]=8
    # (EG): 8 - 4 - A
    EG=eight-four-A
    # (235): [len5]
    _235=[frozenset(x) for x in encoded if len(x)==5]
    # (ADG): 2 n 3 n 5
    ADG=functools.reduce(lambda x, y: x&y,_235)
    # G: (EG) n (ADG)
    G=EG&ADG
    # D: ADG - A - G
    D=ADG-A-G
    # 0: ABCDEFG [8 - D]
    zero=eight-D
    key[0]=zero
    key[zero]=0  
    # E: (EG) - G
    E=EG-G
    # 9: ABCDFG [8 - E]
    nine=eight-E
    key[9]=nine
    key[nine]=9
    # 2: ACDEG (235 containing E)
    two=[x for x in _235 if len(E&x)>0][0]
    key[2]=two
    key[two]=2
    # F: (3^5) - ADG
    _35=[x for x in _235 if x!=two]
    F=functools.reduce(lambda x, y: x&y,_35)-ADG
    # C: 1 - F
    C=one-F
    # 3: ACDFG (235 containing C, is not 2)
    three=[x for x in _235 if len(C&x)>0 and x!=two][0]
    key[3]=three
    key[three]=3
    # 5: ABDFG (235, not 2 or 3)
    five=[x for x in _235 if x not in (two,three)][0]
    key[5]=five
    key[five]=5
    # 6: ABDEFG (5 u E)
    six=five|E
    key[6]=six
    key[six]=6
    #Return key
    return(key)

print(count1478(inp))
print(decode_all(inp))