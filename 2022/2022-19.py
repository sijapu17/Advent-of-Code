#Advent of Code 2022 Day 19

import re, heapq

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-19.txt')
contents = f.read()
inp = contents.splitlines()

global costs, total_time

def ceildiv(a, b):
    return -(a // -b)

costs={}

for line in inp:
#Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    nums=[int(x) for x in re.findall('\d+',line)]
    id=nums[0]
    costs[id]={}
    costs[id]['ore']=nums[1] #Units of ore to make an ore robot
    costs[id]['clay']=nums[2] #Units of ore to make a clay robot    
    costs[id]['obsidian']=(nums[3],nums[4]) #Units of ore, clay to make an obsidian robot   
    costs[id]['geode']=(nums[5],nums[6]) #Units of ore, obsidian to make a geode robot

def best_geode_count(id,total_time): #Return quality level (i.e. best geode production) of a single recipe
        
        #Calculate the most of each robot it's useful to ever have (we can only make 1 robot per minute)
        max_robots={}
        max_robots['ore']=max(costs[id]['ore'],costs[id]['clay'],costs[id]['obsidian'][0],costs[id]['geode'][0])
        max_robots['clay']=costs[id]['obsidian'][1]
        max_robots['obsidian']=costs[id]['geode'][1]

        frontier=[] #Heap of the search frontier, i.e. nodes that have been created but not yet examined
        start_node=Node(id,{'ore':1,'clay':0,'obsidian':0,'geode':0},{'ore':0,'clay':0,'obsidian':0,'geode':0},total_time,'')
        heapq.heappush(frontier,start_node)

        i=0
        while len(frontier)>0:
            current=heapq.heappop(frontier)
            i+=1
            #print(f'i={i} {current}')
            if current.time_rem<=0:
                print(current.materials['geode'])
                return(current.materials['geode'])
            
            #Create new node for each robot it is possible to build next
            new_robot=False
            #1. Ore robot
            if current.robots['ore']<max_robots['ore']:
                new_robot=True
                #New material required to be mined to build robot
                ore_needed=max(0,costs[id]['ore']-current.materials['ore'])
                #Time required to mine any missing material, plus 1 minute to build new robot
                build_dur=ceildiv(ore_needed,current.robots['ore'])+1
                if build_dur<=current.time_rem:
                    materials=current.materials.copy()
                    robots=current.robots.copy()
                    #Update materials and robots
                    for k,v in robots.items():
                        materials[k]+=build_dur*v
                    materials['ore']-=costs[id]['ore']
                    robots['ore']+=1
                    time_rem=current.time_rem-build_dur
                    #Create new node
                    heapq.heappush(frontier,Node(id,robots,materials,time_rem,current.history+'O'))

            #2. Clay robot
            if current.robots['clay']<max_robots['clay']:
                new_robot=True
                #New material required to be mined to build robot
                ore_needed=max(0,costs[id]['clay']-current.materials['ore'])
                #Time required to mine any missing material, plus 1 minute to build new robot
                build_dur=ceildiv(ore_needed,current.robots['ore'])+1
                if build_dur<=current.time_rem:
                    materials=current.materials.copy()
                    robots=current.robots.copy()
                    #Update materials and robots
                    for k,v in robots.items():
                        materials[k]+=build_dur*v
                    materials['ore']-=costs[id]['clay']
                    robots['clay']+=1
                    time_rem=current.time_rem-build_dur
                    #Create new node
                    heapq.heappush(frontier,Node(id,robots,materials,time_rem,current.history+'C'))

            #3. Obsidian robot
            if current.robots['obsidian']<max_robots['obsidian'] and current.robots['clay']>0:
                new_robot=True
                #New material required to be mined to build robot
                ore_needed=max(0,costs[id]['obsidian'][0]-current.materials['ore'])
                clay_needed=max(0,costs[id]['obsidian'][1]-current.materials['clay'])
                #Time required to mine any missing material, plus 1 minute to build new robot
                build_dur=max(ceildiv(ore_needed,current.robots['ore']),ceildiv(clay_needed,current.robots['clay']))+1
                if build_dur<=current.time_rem:
                    materials=current.materials.copy()
                    robots=current.robots.copy()
                    #Update materials and robots
                    for k,v in robots.items():
                        materials[k]+=build_dur*v
                    materials['ore']-=costs[id]['obsidian'][0]
                    materials['clay']-=costs[id]['obsidian'][1]
                    robots['obsidian']+=1
                    time_rem=current.time_rem-build_dur
                    #Create new node
                    heapq.heappush(frontier,Node(id,robots,materials,time_rem,current.history+'B'))

            #4. Geode robot
            if current.robots['obsidian']>0:
                new_robot=True
                #New material required to be mined to build robot
                ore_needed=max(0,costs[id]['geode'][0]-current.materials['ore'])
                obsidian_needed=max(0,costs[id]['geode'][1]-current.materials['obsidian'])
                #Time required to mine any missing material, plus 1 minute to build new robot
                build_dur=max(ceildiv(ore_needed,current.robots['ore']),ceildiv(obsidian_needed,current.robots['obsidian']))+1
                if build_dur<=current.time_rem:
                    materials=current.materials.copy()
                    robots=current.robots.copy()
                    #Update materials and robots
                    for k,v in robots.items():
                        materials[k]+=build_dur*v
                    materials['ore']-=costs[id]['geode'][0]
                    materials['obsidian']-=costs[id]['geode'][1]
                    robots['geode']+=1
                    time_rem=current.time_rem-build_dur
                    #Create new node
                    heapq.heappush(frontier,Node(id,robots,materials,time_rem,current.history+'G'))

            #If no new robots could be created in remaining time, run time to end
            if new_robot==False:
                materials=current.materials.copy()
                robots=current.robots.copy()
                #Update materials and robots
                for k,v in robots.items():
                    materials[k]+=current.time_rem*v
                #Create new node
                heapq.heappush(frontier,Node(id,robots,materials,0,current.history+'#'))

        print("Empty frontier, no solution found")

def sum_quality_levels(total_time): #Return sum of all quality levels for each blueprint
    sum=0
    for k in costs.keys():
        print(f'k={k}')
        sum+=best_geode_count(k,total_time)*k
    return(sum)

def prod_geode_totals(total_time): #Return product of total geodes for first 3 blueprints
    prod=1
    for k in (1,2,3):
        print(f'k={k}')
        prod*=best_geode_count(k,total_time)
    return(prod)

class Node():
    def __init__(self,id,robots,materials,time_rem,history) -> None:
        self.id=id
        self.robots=robots #Dict of current number of each robot
        self.materials=materials #Dict of current stock of each material
        self.time_rem=time_rem #Time remaining
        self.history=history #Robot creation history
        self.g=self.materials['geode']
        #Best-case future geode production (assuming new geode robot built every remaining minute)
        self.h=self.robots['geode']*time_rem + int(time_rem*(time_rem+1)/2)
        self.f=-1*(self.g+self.h)

    def __lt__(self, other):
        return(self.f<other.f)
    
    def __str__(self):
        r=[self.robots[x] for x in ('ore','clay','obsidian','geode')]
        m=[self.materials[x] for x in ('ore','clay','obsidian','geode')]
        return(f'ID={self.id} {self.history} t={self.time_rem} R:{r} M:{m} h={self.h} f={self.f}')

    def __repr__(self):
        return(self.__str__())
        
print(sum_quality_levels(24))
print(prod_geode_totals(32))