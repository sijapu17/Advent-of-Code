#Advent of Code 2024 Day 21

from functools import cache
from dataclasses import dataclass
from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-21.txt')
contents = f.read()
input = contents.splitlines()

dir_coords={'>':complex(1,0),'<':complex(-1,0),'^':complex(0,-1),'v':complex(0,1)}

numpad_in=[['7','8','9'],['4','5','6'],['1','2','3'],['X','0','A']]
numpad={}
for j in range(4):
    for i in range(3):
        if numpad_in[j][i]!='X':
            numpad[numpad_in[j][i]]=complex(i,j)
numpad_coords=set(numpad.values())

dirpad_in=[['X','^','A'],['<','v','>']]
dirpad={}
for j in range(2):
    for i in range(3):
        if dirpad_in[j][i]!='X':
            dirpad[dirpad_in[j][i]]=complex(i,j)
dirpad_coords=set(dirpad.values())

def heuristic(path): #Determine heuristic of path, where lower score is better
    score=0
    dists={'<':4,'v':3,'^':1,'>':1,'A':0} #Travel distances on keypad
    for i in range(len(path)):
        if i>0 and path[i]!=path[i-1]:
            score+=1000 #Penalise changing direction
        score+=i*dists[path[i]] #Prioritise visiting futher keys first
    return(score)

@dataclass
class Node(): #Node for pathfinding
    pos:complex
    path:str

@cache
def pad_to_pad(start,end): #Convert pad code to pad moves
    #Detect whether input is on dirpad or numpad
    if start in '<>v^' or end in '<>v^':
        pad=dirpad
        pad_coords=dirpad_coords
    else:
        pad=numpad
        pad_coords=numpad_coords
    s_pos=pad[start]
    e_pos=pad[end]
    dirs=[] #Only consider up to 2 dirs which move in correct direction
    if e_pos.real>s_pos.real:
        dirs.append('>')
    elif e_pos.real<s_pos.real:
        dirs.append('<')
    if e_pos.imag>s_pos.imag:
        dirs.append('v')
    elif e_pos.imag<s_pos.imag:
        dirs.append('^')
    frontier=[]
    frontier.append(Node(s_pos,''))
    paths=[] #Collect valid paths
    while len(frontier)>0:
        current=frontier.pop()
        if current.pos==e_pos:
            paths.append(current.path+'A')
        else:
            for d in dirs:
                new_pos=current.pos+dir_coords[d]
                if new_pos in pad_coords:
                    frontier.append(Node(new_pos,current.path+d))
    best_path=sorted(paths,key=heuristic)[0]
    return(best_path) #Return best path

@cache
def A_to_A(path): #Expand path between two A presses
    if path=='':
        return('A')
    ret=pad_to_pad('A',path[0])+''.join([pad_to_pad(path[i],path[i+1]) for i in range(len(path)-1)])+pad_to_pad(path[-1],'A')
    return(ret)

#Correct for Part 1, too slow for Part 2
def complexity(path,n): #Expand path out to full path via n computers and calculate complexity score
    numeric=int(path[:-1])
    for _ in range(n):
        path=pad_to_pad('A',path[0])+''.join([pad_to_pad(path[i],path[i+1]) for i in range(len(path)-1)])
    return(numeric*len(path))
    
def complexity(path,n): #Expand path out to full path via n computers and calculate complexity score
    numeric=int(path[:-1])

    segments=defaultdict(int)
    for s in path.split('A')[:-1]:
        segments[s]+=1
    for _ in range(n):    
        new_segments=defaultdict(int)
        for seg, n in segments.items():
            new_path=A_to_A(seg)
            for new_seg in new_path.split('A')[:-1]:
                new_segments[new_seg]+=n
        segments=new_segments
    #Full Length is segment length * each time it appears, plus 1 per segment for the final A press
    full_length=sum([(len(s)+1)*n for s,n in segments.items()])
    return(numeric*full_length)

print(sum([complexity(code,3) for code in input]))
print(sum([complexity(code,26) for code in input]))