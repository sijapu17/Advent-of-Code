#Advent of Code 2021 Day 23

import heapq, copy
f1 = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-23.txt')
contents1 = f1.read()
inp1 = contents1.splitlines()
f2 = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-23p2.txt')
contents2 = f2.read()
inp2 = contents2.splitlines()

class Cave():
    def __init__(self,part,inp,start_cost=0) -> None:
        self.part=part #Part 1 or 2
        self.cost=start_cost #Total energy cost of all crab movement so far
        self.costhistory=[] #For debugging
        self.movehistory='' #For debugging
        self.floor=set() #Coordinates of all floor spaces, including those currently containing a crab
        self.crabs={} #Dict of crabs, using current position as key
        self.dimX=len(inp[0])
        self.dimY=len(inp)
        for j in range(self.dimY): #Create floor map            
            for i in range(self.dimX):
                item=inp[j][i]
                if item in ('ABCD.'):
                    self.floor.add(complex(i,j))
        for j in range(self.dimY): #Create crabs
            for i in range(self.dimX):
                item=inp[j][i]                    
                if item in ('ABCD'):
                    self.crabs[complex(i,j)]=Crab(part,item,complex(i,j),self)
        cols={'A':3,'B':5,'C':7,'D':9} #Columns which each type of crab is trying to reach
        for i in cols.values(): #Assign 'end' status to crabs if they are in correct column and only have same-type crabs below them
            j=self.dimY-2
            while j>1:
                pos=complex(i,j)
                if pos in self.crabs:
                    crab=self.crabs[pos]
                    if cols[crab.type]==i:
                        crab.status='end'
                        j-=1
                    else:
                        j=0
                else:
                    j=0
        self.min_total_cost=self.cost+sum([c.min_remaining_cost for c in self.crabs.values()]) #Minimum total cost
        self.log=self.map() #Log of all maps and moves

    def map(self) -> str: #Create map of room
        ret=f'Cost: {self.cost} ({self.min_total_cost})\n'
        for j in range(self.dimY):
            for i in range(self.dimX):        
                pos=complex(i,j)
                if pos in self.crabs:
                    ret+=self.crabs[pos].type
                elif pos in self.floor:
                    ret+='.'
                else:
                    ret+='#'
            ret+='\n'
        return(ret)

    def __str__(self) -> str:
        return(self.log)

    def __repr__(self) -> str:
        return(f'Cave({self.cost},{self.min_total_cost})')

    def __hash__(self) -> int:
        ret=''
        for j in range(1,self.dimY-1):
            for i in range(1,self.dimX-1):        
                pos=complex(i,j)
                if pos in self.crabs:
                    ret+=self.crabs[pos].type
                else:
                    ret+='#'
        return(hash(ret))

    def all_crabs_home(self): #Check if all crabs have reached end status
        for c in self.crabs.values():
            if c.status!='end':
                return(False)
        return(True)

    def all_possible_moves(self): #List all possible moves for all crabs and immediately perform all endpoint moves
        move_loop=True
        while move_loop:
            end_moves=[] #Moves taking a crab to endpoint
            self.hallway_moves=[] #Moves taking crab to hallway
            for pos,crab in self.crabs.items():
                crab_moves=crab.list_possible_moves()
                for m in crab_moves:
                    move=(pos,m[0],m[1],m[2]) #Move takes the form (start,dest,cost,dest_type)
                    if m[2]=='end':
                        end_moves.append(move)
                    elif m[2]=='hallway':
                        self.hallway_moves.append(move)
            if len(end_moves)>0: #If there are endpoint moves available, do them and check again
                dests=set() #Avoid moving two crabs to same destination
                for em in end_moves: #Possible endpoint moves are always optimal (for the current cave) and will not interfere with other moves
                    if em[1] not in dests:
                        self.move_crab(em)
                        dests.add(em[1])
            else: #If no more endpoint moves, exit function to move onto hallway moves
                move_loop=False


    def move_crab(self,move): #Move a single crab
        crab=self.crabs[move[0]]
        crab.pos=move[1] #Update crab's internal position
        crab.status=move[3] #Change crab status to 'hallway' or 'end' depending on destination
        crab.min_remaining_cost=crab.calc_min_rem_cost()
        del self.crabs[move[0]] #Remove crab from start position
        self.crabs[move[1]]=crab #Add crab to end position
        self.cost+=move[2]
        self.costhistory.append(move[2])
        self.min_total_cost=self.cost+sum([c.min_remaining_cost for c in self.crabs.values()])
        self.movehistory+=f'{crab.type}{str(int(move[0].real))}{str(int(move[0].imag))}{str(int(move[1].real))}{str(int(move[1].imag))}'
        self.log+=crab.type+str(move)+'\n'+self.map()


    def create_copy(self): #Create a copy of Cave object
        return(copy.deepcopy(self))

    def __lt__(self,other): #Order based on minimum total cost
        return(self.min_total_cost<=other.min_total_cost)


class Crab():
    def __init__(self,part,type,pos,cave) -> None:
        self.part=part
        self.type=type
        cols={'A':3,'B':5,'C':7,'D':9} #Columns which each type of crab is trying to reach 
        costs={'A':1,'B':10,'C':100,'D':1000}
        self.cost=costs[self.type] #Cost per move
        self.pos=pos
        self.cave=cave
        if part==1:
            self.endpoints=[complex(cols[type],3),complex(cols[type],2)] #Two possible endpoints for crab
        elif part==2:
            self.endpoints=[complex(cols[type],5),complex(cols[type],4),complex(cols[type],3),complex(cols[type],2)] #Four possible endpoints for crab
        #Crabs have a status of 'start', 'hallway' or 'end' depending on their position
        if self.pos.imag==1:
            self.status='hallway'
        elif self.pos==self.endpoints[0]:
            self.status='end' #If crab starts at its lowest endpoint, it doesn't need to move
        else:
            self.status='start'
            self.hallway_positions=[complex(i,1) for i in range(1,12) if i not in cols.values()] #List of all possible places that the crab can move
        self.min_remaining_cost=self.calc_min_rem_cost()

    def __repr__(self) -> str:
        return(f'{self.type}: {self.pos} ({self.min_remaining_cost})')

    def __str__(self) -> str:
        return(self.__repr__())

    def list_possible_moves(self): #Create a list of all places the crab can move to
        #If crab is already at endpoint, don't consider moving
        if self.status=='end': 
            return([])
        #If other crab of same type is in lowest endpoint, try to go to next endpoint up
        while len(self.endpoints)>0:
            if self.endpoints[0] in self.cave.crabs.keys() and self.cave.crabs[self.endpoints[0]].type==self.type:
                self.endpoints.pop(0)
            else:
                ep=self.endpoints[0]
                break                
        end_cost=self.cost_route(ep)
        end_tuple=(ep,end_cost,'end')
        if type(end_cost) is int: #If endpoint is reachable, don't consider hallway destinations
            return([end_tuple])
        #If endpoint is unreachable and crab hasn't yet moved, consider hallway destinations
        elif self.status=='start':
            possible=[]
            for hall_dest in self.hallway_positions: #Append any reachable hallway position, along with its cost
                hall_cost=self.cost_route(hall_dest)
                if type(hall_cost) is int:
                    possible.append((hall_dest,hall_cost,'hallway'))
            return(possible)
        return([])

    def cost_route(self,dest): #Check whether destination is currently reachable, and provide cost if it is
        c=self.pos #Starting position
        cost=0 #Cost of route
        while c!=dest:
            if c.real!=dest.real: #If horizontal position doesn't match, move to row 1 (hallway) and adjust from there
                if c.imag>1:
                    c+=complex(0,-1)
                    cost+=self.cost
                elif c.real<dest.real:
                    c+=complex(1,0)
                    cost+=self.cost
                elif c.real>dest.real:
                    c+=complex(-1,0)
                    cost+=self.cost
            else: #If horizontal position matches, move down to destination
                c+=complex(0,1)
                cost+=self.cost
            if c in self.cave.crabs.keys(): #If route is blocked by another crab, abort pathfinding
                return(None)
        return(cost)

    def calc_min_rem_cost(self): #Calculate minimum remaining cost for crab to get to end
        if self.status=='end':
            rem=0
        else:
            dist=self.pos.imag-1+abs(self.pos.real-self.endpoints[0].real)+1
            if self.status=='start':
                dist=max(dist,4) #A crab that has to move out of the way of one below must take at least 4 steps
            rem=self.cost*dist
        return(int(rem))

def find_minimal_cost(part,inp,cost=0): #Use A* Algorithm to traverse different cave nodes to find minimal cost
    start_cave=Cave(part,inp,cost)
    frontier=[]
    visited=set() #Track positions that have already been visited to avoid duplication
    heapq.heappush(frontier,start_cave)
    while len(frontier)>0:
        cave=heapq.heappop(frontier) #Examine cave in open heap with lowest cost
        if cave.all_crabs_home():
            print('Solution cave found')
            print(cave.movehistory)
            return(cave)         
        cave.all_possible_moves() #Generate all possible moves and make any endpoint moves
        if hash(cave) in visited:
            continue
        visited.add(hash(cave))
        if cave.all_crabs_home(): #A finished cave at this stage may not be optimal
            heapq.heappush(frontier,cave)
        else:
            for hm in cave.hallway_moves: #Loop over all possible hallway moves and create a new cave node for each
                clone=cave.create_copy()
                clone.move_crab(hm)
                if hash(clone) not in visited:
                    heapq.heappush(frontier,clone)
    print('All caves explored, no solution found')

print(find_minimal_cost(1,inp1))
print(find_minimal_cost(2,inp2,0))