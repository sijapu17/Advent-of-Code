#Advent of Code 2023 Day 12

from functools import cache

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-12.txt')
contents = f.read()
input = contents.splitlines()

rows=[]
for i in input:
    springs=i.split(' ')[0]
    groups=[int(x) for x in i.split(' ')[1].split(',')]
    rows.append((springs,groups))

folded_rows=[]
for i in input:
    springs=i.split(' ')[0]
    folded_springs=springs+'?'+springs+'?'+springs+'?'+springs+'?'+springs
    groups=[int(x) for x in i.split(' ')[1].split(',')]
    folded_groups=5*groups
    folded_rows.append((folded_springs,folded_groups))

@cache
def n_arrangements(springs: str,groups: tuple):

    if debug=='Y':
        print(f'{springs},{groups}')

    if len(springs)==0:
        if len(groups)==0:
            if debug=='Y':
                print('Match')
            return(1)
        else:
            return(0)
    
    #Case where first spring is working
    if springs[0]=='.':
        return(n_arrangements(springs[1:],groups))

    #Case where first spring is broken
    elif springs[0]=='#':
        if len(groups)==0:
            return(0)
        else:
            size=groups[0]
            if size>len(springs):
                return(0)
            else:
                #If group contains . or next spring after group is #, group cannot start here
                if (len(springs)>size and springs[size]=='#') or '.' in springs[:size]:
                    return(0)
                #Otherwise, group must start here
                else:
                    return(n_arrangements(springs[size+1:],groups[1:]))
        
    #Case where first spring is unknown
    elif springs[0]=='?':
        return(n_arrangements('.'+springs[1:],groups)+n_arrangements('#'+springs[1:],groups))
    
debug='N'
    
#print(n_arrangements('???',[1,1]))

#r=0
#print(n_arrangements(rows[r][0],rows[r][1]))

#for row in rows:
#    print(n_arrangements(row[0],row[1]))

def count_score(rows):
    return(sum(n_arrangements(r[0],tuple(r[1])) for r in rows))

print(count_score(rows))
print(count_score(folded_rows))