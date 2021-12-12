#Advent of Code 2021 Day 10
import statistics

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-10.txt')
contents = f.read()
inp = contents.splitlines()

def score_corrupted(inp): #Score input lines which are corrupt
    score=0
    score_ref={')':3,']':57,'}':1197,'>':25137}
    for line in inp:
        stack=[]
        for c in line:
            if c in '([{<':
                stack.append(c)
            else:                 
                partner=stack.pop()
                if partner+c not in ('()','[]','{}','<>'): #Case of mismatching bracket - corrupt line
                    score+=score_ref[c]
                    break
    return(score)

def score_incomplete(inp): #Count number of input lines which are corrupt
    scores=[]
    score_ref={'(':1,'[':2,'{':3,'<':4}
    for line in inp:
        corrupt=False
        stack=[]
        for c in line:
            if c in '([{<':
                stack.append(c)
            else:                 
                partner=stack.pop()
                if partner+c not in ('()','[]','{}','<>'): #Case of mismatching bracket - corrupt line, do not score
                    corrupt=True
                    break
        if not corrupt:
            #At end of incomplete line, score brackets that need to be added
            score=0
            while len(stack)>0:
                bracket=stack.pop()
                score*=5
                score+=score_ref[bracket]
            scores.append(score)
    return(int(statistics.median(scores)))

print(score_corrupted(inp))
print(score_incomplete(inp)) #850753009 too low