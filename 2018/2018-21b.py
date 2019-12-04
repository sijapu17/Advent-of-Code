#Advent of Code 2018 Day 21 Part 2
import math

def solveB():
    a=0
    c=0
    seen=set()
    previous=None
    while True:
        a=c|65536
        c=10828530        
        while True:
            #print('a='+str(a)+' c='+str(c))
            #c+=(a&255)
            #c&=16777215
            #c*=65889
            #c&=16777215
            c = (((c + (a & 255)) & 16777215) * 65899) & 16777215
            if 256>a: #Generate
                print(str(c))
                if c in seen:
                    return(previous)
                seen.add(c)
                previous=c
                break
            else:
                a=a//256
                
#retB=solveB() #16773073 too high

def run_activation_system(magic_number):
    seen = set()
    c = 0
    last_unique_c = -1

    while True:
        a = c | 65536
        c = magic_number

        while True:
            c = (((c + (a & 255)) & 16777215) * 65899) & 16777215

            if 256 > a:
                if c not in seen:
                    seen.add(c)
                    print(c)
                    last_unique_c = c
                    break
                else:
                    return(last_unique_c)
            else:
                a //= 256
                
#retB_=run_activation_system(10828530) #11777564 - correct

def test(a,c):
    c0=c
    a0=a
    
    b=a&255
    c+=b
    c&=16777215
    c*=65889
    c&=16777215
    print('a='+str(a)+' c='+str(c))
    
    c=c0
    a=a0
    c = (((c + (a & 255)) & 16777215) * 65899) & 16777215
    print('a='+str(a)+' c='+str(c))
    
test(a=39,c=41)
