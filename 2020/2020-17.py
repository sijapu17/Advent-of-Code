#Advent of Code 2020 Day 17


f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-17.txt')
state = f.read()
input=state.splitlines()

class Cubes():
    def __init__(self,input):
        self.locs=set() #Set of active cube locations
        l=0
        k=0
        j=0
        for row in input:
            i=0
            for g in row:
                if g=='#': #Switch to a letter so uppercase/lowercase can be used during update procedure
                    self.locs.add((i,j,k,l))
                i+=1
            j+=1

    def update_bounds(self):
        #Find bounds of map
        self.minX=min(self.locs,key=lambda x:x[0])[0]
        self.maxX=max(self.locs,key=lambda x:x[0])[0]
        self.minY=min(self.locs,key=lambda x:x[1])[1]
        self.maxY=max(self.locs,key=lambda x:x[1])[1]
        self.minZ=min(self.locs,key=lambda x:x[2])[2]
        self.maxZ=max(self.locs,key=lambda x:x[2])[2]
        self.minW=min(self.locs,key=lambda x:x[3])[3]
        self.maxW=max(self.locs,key=lambda x:x[3])[3]

    def nAdjacent(self,pos): #For a given position, check how many of its 8 neighbours are equal to state
        count=0
        for i in (-1,0,1):
            for j in (-1,0,1):
                for k in (-1,0,1):
                    for l in (-1,0,1):
                        nPos=(pos[0]+i,pos[1]+j,pos[2]+k,pos[3]+l)
                        if nPos in self.locs and pos!=nPos: #Do not count cube as its own neighbour                        
                            count+=1
        return(count)

    def update(self,part): #Check adjacent seats and update each seat
        self.update_bounds() #Update bounds as they will expand over time
        to_add=set() #Cubes that will be added after current state
        to_remove=set() #Cubes that will be removed after current state
        #For each dimension, check from 1 before the min to 1 after the max
        for i in range(self.minX-1,self.maxX+2):
            for j in range(self.minY-1,self.maxY+2):
                for k in range(self.minZ-1,self.maxZ+2):
                    for l in range(self.minW-1,self.maxW+2):
                        if l==0 or part==2: #For part 1 only consider 3 dimensions
                            pos=(i,j,k,l)
                            if pos in self.locs:
                                if self.nAdjacent(pos) not in (2,3):
                                    to_remove.add(pos)
                            else:
                                if self.nAdjacent(pos)==3:
                                    to_add.add(pos)

        self.locs-=to_remove
        self.locs|=to_add

    def update_n_times(self,n,part):
        for x in range(n):
            self.update(part)

    def count_active(self): #Return number of active cubes
        return(len(self.locs))

#Part 1
cubes=Cubes(input)
cubes.update_n_times(6,1)
print(cubes.count_active())
#Part 2
cubes=Cubes(input)
cubes.update_n_times(6,2)
print(cubes.count_active())