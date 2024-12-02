#Advent of Code 2024 Day 2

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-02.txt')
contents = f.read()
input = [[int(y) for y in x.split()] for x in contents.splitlines()]

def is_safe(r):
    diffs=[r[i+1]-r[i] for i in range(len(r)-1)]
    if (min(diffs)>=-3 and max(diffs)<=-1) or (min(diffs)>=1 and max(diffs)<=3):
        #print(f'Safe: {r}')
        return(True)
    else:
        #print(f'Unsafe: {r}')
        return(False)

#Part 1
print(sum([is_safe(r) for r in input]))

#Part 2
safe=0
for r in input:
    for i in range(len(r)):
        if is_safe(r[:i]+r[i+1:]):
            safe+=1
            break

print(safe)