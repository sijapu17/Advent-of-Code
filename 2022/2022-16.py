#Advent of Code 2022 Day 16

import re, heapq
from collections import deque

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-16.txt')
contents = f.read()
inp = contents.splitlines()

class Volcano():
    def __init__(self,inp,time) -> None:
        self.time=time
        self.v_rates={}
        self.v_nebrs={}
        self.endpoints=set(['AA']) #Only valves with non-zero rates (and start valve AA) are potential
                                   #stops on the A* traversal
        self.dists={} #Distances between endpoints
        #Parse valve data
        p=re.compile("Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)")
        for l in inp:
            m=p.match(l)
            id=m.group(1)
            rate=int(m.group(2))
            self.v_rates[id]=rate
            self.v_nebrs[id]=m.group(3).split(', ')
            if rate>0:
                self.endpoints.add(id)
        #Calculate distances between each valve
        for e in self.endpoints:
            self.dists[e]={}
            frontier=deque()
            frontier.append(Dist_Node(e,0,set()))
            #Continue until all other endpoints have been reached
            while len(self.dists[e])+1<len(self.endpoints):
                current=frontier.popleft()
                loc=current.loc
                current.visited.add(loc)
                #Add location to dists dict if found for the first time
                if loc in self.endpoints and loc not in self.dists[e] and loc!=e:
                    self.dists[e][loc]=current.dist+1 #Add 1 to account for time to open valve
                for nebr in self.v_nebrs[loc]:
                    if nebr not in self.dists[e]:
                        frontier.append(Dist_Node(nebr,current.dist+1,current.visited.copy()))
        self.endpoints.remove('AA') #Paths should never revisit AA

    #Using BFS, find largest amount of pressure that can be released for each set of opened valves
    def find_best_paths(self):
        self.best_paths={}
        frontier=deque()
        frontier.append(Path_Node('AA',0,self.time,set()))
        while len(frontier)>0:
            current=frontier.popleft()
            loc=current.loc       
            for e in self.endpoints:
                if e not in current.open_valves:
                    time_rem=max(0,current.time_rem-self.dists[loc][e])
                    if time_rem>0:
                        pressure_released=current.pressure_released+time_rem*self.v_rates[e]
                        open_valves=current.open_valves.copy()
                        open_valves.add(e)
                        #Memoise best release for this set of open valves
                        key=frozenset(open_valves)
                        if key not in self.best_paths or (key in self.best_paths and pressure_released>self.best_paths[key]):
                            self.best_paths[key]=pressure_released
                        frontier.append(Path_Node(e,pressure_released,time_rem,open_valves))
        best_single=max(self.best_paths.values())
        print(f'Best single path released {best_single} pressure')
            
    #Find best pair of paths to maximise pressure release
    def find_best_pair(self):
        best=0
        for ak, av in self.best_paths.items():
            for bk, bv in self.best_paths.items():
                if len(ak)>=len(bk) and ak.isdisjoint(bk):
                    best=max(best,av+bv)
        return(best)

class Path_Node(): #BFS Node to find best release for each subset of opened valves
    def __init__(self,loc,pressure_released,time_rem,open_valves) -> None:
        self.loc=loc
        self.pressure_released=pressure_released
        self.time_rem=time_rem
        self.open_valves=open_valves

class Dist_Node(): #BFS node for initial distance calculation
    def __init__(self,loc,dist,visited) -> None:
        self.loc=loc
        self.dist=dist
        self.visited=visited

volcano=Volcano(inp,30)
volcano.find_best_paths()
volcano=Volcano(inp,26)
volcano.find_best_paths()
print(volcano.find_best_pair())
#print(volcano.best_paths)
#print(volcano.find_best_path())
