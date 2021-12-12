#Advent of Code 2021 Day 12

from collections import defaultdict, deque
import collections
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-12.txt')
contents = f.read()
inp = contents.splitlines()

class Cave():
    def __init__(self,inp) -> None:
        self.links=defaultdict(list) #Dict of all links between neighbouring caves
        for line in inp: #Add each link in both directions
            self.links[line.split('-')[0]].append(line.split('-')[1])
            self.links[line.split('-')[1]].append(line.split('-')[0])

    def count_all_paths(self): #Find and count all paths in cave, using BFS
        count=0
        frontier=deque()
        frontier.append(Node()) #Start node
        
        while len(frontier)>0:
            current=frontier.popleft()
            #print(current)
            if current.pos=='end':
                #print(current.path)
                count+=1
            else:
                for dest in self.links[current.pos]: #From current pos, create a new node traversing to each neighbouring cave as long as it's not a repeated small cave
                    if dest not in current.smalls_visited:
                        p=current.path[:] #Copy of path
                        p.append(dest)
                        frontier.append(Node(pos=dest,smalls_visited=current.smalls_visited.copy(),path=p))
        return(count)

    def count_all_paths2(self): #Find and count all paths in cave, using BFS
        count=0
        frontier=deque()
        frontier.append(Node2()) #Start node
        
        while len(frontier)>0:
            current=frontier.popleft()
            #print(current)
            if current.pos=='end':
                #print(current.path)
                count+=1
            else:
                for dest in self.links[current.pos]: #From current pos, create a new node traversing to each neighbouring cave as long as it's not a repeated small cave
                    if (len(current.smalls_visited_twice)==0 or dest not in current.smalls_visited) and dest!='start':
                        p=current.path[:] #Copy of path
                        p.append(dest)
                        frontier.append(Node2(pos=dest,smalls_visited=current.smalls_visited.copy(),smalls_visited_twice=current.smalls_visited_twice.copy(),path=p))
        return(count)

class Node(): #BFS node for cave traversal
    def __init__(self,pos='start',smalls_visited=set(['start']),path=['start']) -> None:
        self.pos=pos
        self.smalls_visited=smalls_visited #Set of all small caves visited on path so far, to avoid repeats
        self.path=path #Path taken through cave so far
        if pos.islower():
            smalls_visited.add(pos)

    def __str__(self) -> str:
        return(str(self.path))



class Node2(): #BFS node for cave traversal
    def __init__(self,pos='start',smalls_visited=set(['start']),smalls_visited_twice=set(),path=['start']) -> None:
        self.pos=pos
        self.smalls_visited=smalls_visited #Set of all small caves visited on path so far, to avoid repeats
        self.smalls_visited_twice=smalls_visited_twice
        self.path=path #Path taken through cave so far
        if pos.islower() and pos!='start':
            if pos in smalls_visited:
                smalls_visited_twice.add(pos)
            else:
                smalls_visited.add(pos)

    def __str__(self) -> str:
        return(str(self.path))

#cave=Cave(inp)
#print(cave.count_all_paths())
cave=Cave(inp)
print(cave.count_all_paths2())