#Advent of Code 2022 Day 16

import re, heapq
from collections import deque

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-16.txt')
contents = f.read()
inp = contents.splitlines()

class Volcano():
    def __init__(self,inp) -> None:
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
            frontier.append(BFS_node(e,0,set()))
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
                        frontier.append(BFS_node(nebr,current.dist+1,current.visited.copy()))

    def find_best_path(self): #Using A* algorithm, find path that releases most pressure
        frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
        visited=set() #Visited states of closed valves
        start_node=A_Node('AA',['AA'],0,30,self.endpoints.copy(),self.v_rates,self.dists)
        heapq.heappush(frontier,start_node)
        i=0
        while len(frontier)>0:
            node=heapq.heappop(frontier) #Examine node in open heap with lowest f
            i+=1
            if i%1000==1:
                print(node)
             #Check if node has reached end of time period
            if node.time_rem<=0:
                print('Solution node found')
                return(node)
            elif node.state() in visited:
                continue
            else:
                node.closed_valves.remove(node.loc)
                visited.add(node.state())
                #Open valve
                if self.v_rates[node.loc]>0:
                    node.g+=node.time_rem*self.v_rates[node.loc] #Valve will release pressure for each remaining minute
                #If all valves are open, create final node
                if len(node.closed_valves)==0:
                    heapq.heappush(frontier,A_Node(node.loc,node.path,node.g,0,node.closed_valves.copy(),self.v_rates,self.dists))
                    continue
                #Else, Create new node for each unvisited endpoint
                for n_loc in node.closed_valves:
                    path=node.path+[n_loc]
                    time_rem=node.time_rem-self.dists[node.loc][n_loc] #Subtract travel time to new nebr
                    heapq.heappush(frontier,A_Node(n_loc,path,node.g,time_rem,node.closed_valves.copy(),self.v_rates,self.dists))
        print('All nodes explored, no solution found')

    def find_best_path_2(self): #Using A* algorithm, find path that releases most pressure with two travellers
        frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
        visited=set() #Visited states of closed valves
        closed_valves=self.endpoints-set(['AA'])
        start_node=Dual_Node(['AA','AA'],[['AA'],['AA']],0,[0,0],26,closed_valves,self.v_rates,self.dists)
        heapq.heappush(frontier,start_node)
        i=0
        while len(frontier)>0:
            node=heapq.heappop(frontier) #Examine node in open heap with lowest f
            i+=1
            if i%1000==1:
                print(f'{i}: {node}')
            elif node.state() in visited:
                continue
            #Fast forward to next time of interest
            t=min(min(node.travel_rem),node.time_rem)
            if t>0:
                node.travel_rem=[x-t for x in node.travel_rem]
                node.time_rem-=t
            #Check if node has no potential pressure left
            if node.h==0:
                print('Solution node found')
                print(f'{i}: {node}')
                return(node)
            #Check if first traveller is at a new closed valve
            elif node.travel_rem[0]==0:
                visited.add(node.state())
                #If all valves are open, create final node
                if len(node.closed_valves)==0:
                    travel_rem=[9999,node.travel_rem[1]] #Stop traveller from moving again
                    heapq.heappush(frontier,Dual_Node(node.loc,node.path,node.g,travel_rem,node.time_rem,node.closed_valves.copy(),self.v_rates,self.dists))
                    continue
                #Else, Create new node for each unvisited endpoint
                for n_loc in node.closed_valves:
                    #Open valve
                    closed_valves=node.closed_valves-set([n_loc])
                    dist=self.dists[node.loc[0]][n_loc]
                    dur=max(node.time_rem-dist,0) #Time remaining once valve is reached
                    g=node.g+dur*self.v_rates[n_loc] #Valve will release pressure for each remaining minute
                    path=[node.path[0]+[n_loc],node.path[1]]
                    travel_rem=[dist,node.travel_rem[1]]
                    locs=[n_loc,node.loc[1]]
                    heapq.heappush(frontier,Dual_Node(locs,path,g,travel_rem,node.time_rem,closed_valves,self.v_rates,self.dists))
            #Check if second traveller is at a new closed valve
            elif node.travel_rem[1]==0:
                visited.add(node.state())
                #If all valves are open, create final node
                if len(node.closed_valves)==0:
                    travel_rem=[node.travel_rem[0]] #Stop traveller from moving again
                    heapq.heappush(frontier,Dual_Node(node.loc,node.path,node.g,travel_rem,node.time_rem,node.closed_valves.copy(),self.v_rates,self.dists))
                    continue
                #Else, Create new node for each unvisited endpoint
                for n_loc in node.closed_valves:
                    #Open valve
                    closed_valves=node.closed_valves-set([n_loc])
                    dist=self.dists[node.loc[1]][n_loc]
                    dur=max(node.time_rem-dist,0) #Time remaining once valve is reached
                    g=node.g+dur*self.v_rates[n_loc] #Valve will release pressure for each remaining minute
                    path=[node.path[0],node.path[1]+[n_loc]]
                    travel_rem=[node.travel_rem[0],dist]
                    locs=[node.loc[0],n_loc]
                    heapq.heappush(frontier,Dual_Node(locs,path,g,travel_rem,node.time_rem,closed_valves,self.v_rates,self.dists))
        print('All nodes explored, no solution found')


class Dual_Node(): #A* node for two travellers
    def __init__(self,loc:list,path,pressure_released,travel_rem,time_rem,closed_valves,v_rates,dists):
        self.loc=loc #List pair of locations
        self.path=path
        self.time_rem=time_rem
        self.travel_rem=travel_rem
        self.closed_valves=closed_valves
        self.g=pressure_released #g in A* algorithm (total pressure released so far)
        #h in A* algorithm (overestimate of potential release from now to end)           
        self.h=sum([max(0,self.time_rem)*v_rates[x] for x in self.closed_valves])
        self.f=-1*(self.g+self.h) #Negate f as we are maximising pressure release rather than minimising
   
    def state(self): #State of closed valves for comparison with other nodes
        return(tuple(self.travel_rem+self.loc+sorted(self.closed_valves)))
    
    def __lt__(self, other):
        return(self.f<other.f)

    def __str__(self) -> str:
        return(f'{self.path}, rem={self.time_rem}m, g={self.g}, h={self.h} f={self.f}')

    def __repr__(self) -> str:
        return(self.__str__())
    

class A_Node(): #A* Node for 1 traveller
    def __init__(self,loc,path,pressure_released,time_rem,closed_valves,v_rates,dists):
        self.loc=loc
        self.path=path
        self.time_rem=time_rem
        self.closed_valves=closed_valves
        self.g=pressure_released #g in A* algorithm (total pressure released so far)
        #h in A* algorithm (overestimate of potential release from now to end)
        self.h=sum([max(0,self.time_rem-dists[loc][x])*v_rates[x] for x in self.closed_valves if x!=loc])+max(0,self.time_rem)*v_rates[loc]
        self.f=-1*(self.g+self.h) #Negate f as we are maximising pressure release rather than minimising
   
    def state(self): #State of closed valves for comparison with other nodes
        return(tuple([self.loc]+sorted(self.closed_valves)))
    
    def __lt__(self, other):
        return(self.f<other.f)

    def __str__(self) -> str:
        return(f'{self.path}, rem={self.time_rem}m, g={self.g}, h={self.h}')

    def __repr__(self) -> str:
        return(self.__str__())
    
class BFS_node(): #BFS node for initial distance calculation
    def __init__(self,loc,dist,visited) -> None:
        self.loc=loc
        self.dist=dist
        self.visited=visited

volcano=Volcano(inp)
#print(volcano.dists)
#print(volcano.find_best_path())
print(volcano.find_best_path_2())