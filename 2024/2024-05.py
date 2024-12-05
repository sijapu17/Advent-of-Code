#Advent of Code 2024 Day 5

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-05.txt')
contents = f.read()
input = contents.splitlines()

#Split input into rules and manuals
rules = [[int(y) for y in x.split('|')] for x in input[:input.index('')]]
manuals = [[int(y) for y in x.split(',')] for x in input[input.index('')+1:]]

#Part 1
correct_total=0 #Count correct manual midpoints for Part 1
incorrect_total=0 #Count ordered midpoints of incorrect manuals for part 2
for m in manuals:
    correct=True
    for r in rules: #Check each rule for correctness
        if r[0] in m and r[1] in m and m.index(r[1])<m.index(r[0]):
            correct=False
            break
    if correct:
        correct_total+=m[int(len(m)/2)] #If manual is correct, add value of middle page to total
    else: #Incorrect manuals
        ordered=[m[0]]
        for p in m[1:]: #Loop through remaining pages
            afters={r[1] for r in rules if r[0]==p and r[1] in set(ordered)} #Find pages that are already in the ordered manual and must come after p
            if len(afters)==0:
                ordered.append(p)
            else:
                ordered.insert(min([ordered.index(x) for x in afters]),p)
        incorrect_total+=ordered[int(len(ordered)/2)]

print(correct_total)
print(incorrect_total)