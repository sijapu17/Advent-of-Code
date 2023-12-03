#Advent of Code 2023 Day 3
from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-03.txt')
contents = f.read()
input = contents.splitlines()

#All directions in complex plane
dirs=[complex(1,-1),
            complex(1,0),
            complex(1,1),
            complex(0,1),
            complex(-1,1),
            complex(-1,0),
            complex(-1,-1),
            complex(0,-1)]

#Test whether coordinate is adjacent to a symbol
def any_adjacent_symbol(c:complex,symbols:dict):
    for d in dirs:
        if c+d in symbols.keys():
            return(True)
    return(False)

#Return coordinate of adjacent gear
def adjacent_gear_loc(c:complex,symbols:dict):
    for d in dirs:
        if c+d in symbols.keys() and symbols[c+d]=='*':
            return(c+d)

#Import schematic
digits={}
symbols={}
for j in range(len(input)):
    for i in range(len(input[0])):
        c=input[j][i]
        if c.isdigit():
            digits[complex(i,j)]=c
        elif c!='.':
            symbols[complex(i,j)]=c

def part_numbers_and_gear_ratios(digits:dict,symbols:dict):
    digits_rem=digits.copy()
    part_sum=0
    gears=defaultdict(list)
    while len(digits_rem)>0:
        to_remove=[] #Coordinates to remove once processed

        c=min(digits_rem.keys(),key=lambda x: (x.imag,x.real)) #Find next digit start, starting as leftmost and then upmost as possible
        digit_text=digits_rem[c]
        symbol_found=any_adjacent_symbol(c,symbols) #Flag for whether any digit in current number is adjacent to a symbol
        gear_loc=adjacent_gear_loc(c,symbols) #Save location of adjacent gear, if any
        to_remove.append(c)
        #Find any remaining digits in number
        while c+1 in digits_rem.keys():
            c+=1
            digit_text+=digits_rem[c]
            if not symbol_found:
                symbol_found=any_adjacent_symbol(c,symbols) #Flag for whether any digit in current number is adjacent to a symbol
            if gear_loc is None:
                gear_loc=adjacent_gear_loc(c,symbols) #Save location of adjacent gear, if any
            to_remove.append(c)
        #Add number to part_sum if adjacent to a symbol
        if symbol_found:
            part_sum+=int(digit_text)
        #If adjacent gear found, add to dict
        if gear_loc is not None:
            gears[gear_loc].append(int(digit_text))
        #Remove any checked digit coords
        for r in to_remove:
            del digits_rem[r]
        symbol_found=False #Reset flag
        gear_loc=None #Reset flag
    #Sum of gear ratios
    gear_sum=0
    for parts in gears.values():
        if len(parts)==2:
            gear_sum+=(parts[0]*parts[1])
    print(f'part_sum={part_sum}, gear_sum={gear_sum}')
   
part_numbers_and_gear_ratios(digits,symbols)