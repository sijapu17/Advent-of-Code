#Advent of Code 2021 Day 22

import re
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-22.txt')
contents = f.read()
inp = contents.splitlines()

class Cuboid():
    def __init__(self,x0,x1,y0,y1,z0,z1):
        self.x0=min(x0,x1)
        self.x1=max(x0,x1)
        self.y0=min(y0,y1)
        self.y1=max(y0,y1)
        self.z0=min(z0,z1)
        self.z1=max(z0,z1)

    def area(self): #Return area of cuboid
        return((self.x1-self.x0+1)*(self.y1-self.y0+1)*(self.z1-self.z0+1))

    def any_overlap(self,other): #Boolean determining if two cubes overlap at all
        return(self.x1>=other.x0 and other.x1>=self.x0) and (self.y1>=other.y0 and other.y1>=self.y0) and (self.z1>=other.z0 and other.z1>=self.z0)

    def __str__(self) -> str:
        return(self.__repr__())

    def __repr__(self) -> str:
        return(f'x=({self.x0},{self.x1}),y=({self.y0},{self.y1}),z=({self.z0},{self.z1})')

    def __eq__(self, other) -> bool:
        return(self.x0==other.x0 and self.y0==other.y0 and self.z0==other.z0 and self.x1==other.x1 and self.y1==other.y1 and self.z1==other.z1)

    def __hash__(self) -> int:
        return(hash((self.x0,self.y0,self.z0,self.x1,self.y1,self.z1)))

class Reactor():
    def __init__(self,inp):
        self.cuboids=[] #List of cuboids that are currently switched on
        self.steps=[]
        p=re.compile('(^\w+) x=(\-?\d+)\.\.(\-?\d+),y=(\-?\d+)\.\.(\-?\d+),z=(\-?\d+)\.\.(\-?\d+)$') #Regex pattern to read in instructions
        for line in inp:
            m=p.match(line)
            step=m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6)),int(m.group(7))
            self.steps.append(step)

    def run_reboot(self,part):
        for s in self.steps:
            #print(f'Step {s}')
            type,x0,x1,y0,y1,z0,z1=s #Assign each element of step to correct meaning
            if part==1: #Bounding for part 1 only
                if max(x0,y0,z0)>50 or min(x1,y1,z1)<-50: #If cuboid is fully outside (-50,50) range, skip entirely
                    continue
                else: #If cuboid is partly outside range, only consider section within (-50,50)
                    x0=max(-50,x0)
                    y0=max(-50,y0)
                    z0=max(-50,z0)
                    x1=min(50,x1)
                    y1=min(50,y1)
                    z1=min(50,z1)
            new=Cuboid(x0,x1,y0,y1,z0,z1)
            new_cuboids=[] #At the end of the step, overwrite the old list of cuboids with this
            for cub in self.cuboids:
                #print(f'Cub={str(cub)}')
                #print(f'New={str(new)}')
                if new.any_overlap(cub): #If there is any overlap, partition existing cuboid into smaller cuboids and keep those that do not intersect the new one 
                    x_ranges=[]
                    y_ranges=[]
                    z_ranges=[]
                    #Case where both starts and ends match
                    if cub.x0==new.x0 and cub.x1==new.x1:
                        x_ranges.append((new.x0,new.x1))
                    #Cases where starts match
                    elif cub.x0==new.x0 and cub.x1<new.x1:
                        x_ranges.append((new.x0,cub.x1))
                        x_ranges.append((cub.x1+1,new.x1))                        
                    elif cub.x0==new.x0 and new.x1<cub.x1:
                        x_ranges.append((new.x0,new.x1))
                        x_ranges.append((new.x1+1,cub.x1))
                    #Cases where ends match
                    elif cub.x1==new.x1 and cub.x0<new.x0:
                        x_ranges.append((cub.x0,new.x0-1))
                        x_ranges.append((new.x0,new.x1))
                    elif cub.x1==new.x1 and new.x0<cub.x0:
                        x_ranges.append((new.x0,cub.x0-1))
                        x_ranges.append((cub.x0,new.x1))
                    #n1=c0 case
                    elif new.x0<new.x1==cub.x0<cub.x1:
                        x_ranges.append((new.x0,new.x1-1))
                        x_ranges.append((new.x1,cub.x0))
                        x_ranges.append((new.x1+1,cub.x1))
                    #n0=c1 case
                    elif cub.x0<new.x0==cub.x1<new.x1:
                        x_ranges.append((cub.x0,cub.x1-1))
                        x_ranges.append((cub.x1,new.x0))
                        x_ranges.append((new.x0+1,new.x1))                           
                    #cncn case
                    elif cub.x0<new.x0<cub.x1<new.x1:
                        x_ranges.append((cub.x0,new.x0-1))
                        x_ranges.append((new.x0,cub.x1))
                        x_ranges.append((cub.x1+1,new.x1))
                    #cnnc case
                    elif cub.x0<new.x0<=new.x1<cub.x1:
                        x_ranges.append((cub.x0,new.x0-1))
                        x_ranges.append((new.x0,new.x1))
                        x_ranges.append((new.x1+1,cub.x1))
                    #ncnc case
                    elif new.x0<cub.x0<new.x1<cub.x1:
                        x_ranges.append((new.x0,cub.x0-1))
                        x_ranges.append((cub.x0,new.x1))
                        x_ranges.append((new.x1+1,cub.x1))
                    #nccn case
                    elif new.x0<cub.x0<=cub.x1<new.x1:
                        x_ranges.append((new.x0,cub.x0-1))
                        x_ranges.append((cub.x0,cub.x1))
                        x_ranges.append((cub.x1+1,new.x1))
                    else:
                        print('Error, x ranges not found') 

                    #Case where both starts and ends match
                    if cub.y0==new.y0 and cub.y1==new.y1:
                        y_ranges.append((new.y0,new.y1))
                    #Cases where starts match
                    elif cub.y0==new.y0 and cub.y1<new.y1:
                        y_ranges.append((new.y0,cub.y1))
                        y_ranges.append((cub.y1+1,new.y1))                        
                    elif cub.y0==new.y0 and new.y1<cub.y1:
                        y_ranges.append((new.y0,new.y1))
                        y_ranges.append((new.y1+1,cub.y1))
                    #Cases where ends match
                    elif cub.y1==new.y1 and cub.y0<new.y0:
                        y_ranges.append((cub.y0,new.y0-1))
                        y_ranges.append((new.y0,new.y1))
                    elif cub.y1==new.y1 and new.y0<cub.y0:
                        y_ranges.append((new.y0,cub.y0-1))
                        y_ranges.append((cub.y0,new.y1))
                    #n1=c0 case
                    elif new.y0<new.y1==cub.y0<cub.y1:
                        y_ranges.append((new.y0,new.y1-1))
                        y_ranges.append((new.y1,cub.y0))
                        y_ranges.append((new.y1+1,cub.y1))
                    #n0=c1 case
                    elif cub.y0<new.y0==cub.y1<new.y1:
                        y_ranges.append((cub.y0,cub.y1-1))
                        y_ranges.append((cub.y1,new.y0))
                        y_ranges.append((new.y0+1,new.y1)) 
                    #cncn case
                    elif cub.y0<new.y0<cub.y1<new.y1:
                        y_ranges.append((cub.y0,new.y0-1))
                        y_ranges.append((new.y0,cub.y1))
                        y_ranges.append((cub.y1+1,new.y1))
                    #cnnc case
                    elif cub.y0<new.y0<=new.y1<cub.y1:
                        y_ranges.append((cub.y0,new.y0-1))
                        y_ranges.append((new.y0,new.y1))
                        y_ranges.append((new.y1+1,cub.y1))
                    #ncnc case
                    elif new.y0<cub.y0<new.y1<cub.y1:
                        y_ranges.append((new.y0,cub.y0-1))
                        y_ranges.append((cub.y0,new.y1))
                        y_ranges.append((new.y1+1,cub.y1))
                    #nccn case
                    elif new.y0<cub.y0<=cub.y1<new.y1:
                        y_ranges.append((new.y0,cub.y0-1))
                        y_ranges.append((cub.y0,cub.y1))
                        y_ranges.append((cub.y1+1,new.y1))
                    else:
                        print('Error, y ranges not found') 

                     #Case where both starts and ends match
                    if cub.z0==new.z0 and cub.z1==new.z1:
                        z_ranges.append((new.z0,new.z1))
                    #Cases where starts match
                    elif cub.z0==new.z0 and cub.z1<new.z1:
                        z_ranges.append((new.z0,cub.z1))
                        z_ranges.append((cub.z1+1,new.z1))                        
                    elif cub.z0==new.z0 and new.z1<cub.z1:
                        z_ranges.append((new.z0,new.z1))
                        z_ranges.append((new.z1+1,cub.z1))
                    #Cases where ends match
                    elif cub.z1==new.z1 and cub.z0<new.z0:
                        z_ranges.append((cub.z0,new.z0-1))
                        z_ranges.append((new.z0,new.z1))
                    elif cub.z1==new.z1 and new.z0<cub.z0:
                        z_ranges.append((new.z0,cub.z0-1))
                        z_ranges.append((cub.z0,new.z1))
                    #n1=c0 case
                    elif new.z0<new.z1==cub.z0<cub.z1:
                        z_ranges.append((new.z0,new.z1-1))
                        z_ranges.append((new.z1,cub.z0))
                        z_ranges.append((new.z1+1,cub.z1))
                    #n0=c1 case
                    elif cub.z0<new.z0==cub.z1<new.z1:
                        z_ranges.append((cub.z0,cub.z1-1))
                        z_ranges.append((cub.z1,new.z0))
                        z_ranges.append((new.z0+1,new.z1))                  
                    #cncn case
                    elif cub.z0<new.z0<cub.z1<new.z1:
                        z_ranges.append((cub.z0,new.z0-1))
                        z_ranges.append((new.z0,cub.z1))
                        z_ranges.append((cub.z1+1,new.z1))
                    #cnnc case
                    elif cub.z0<new.z0<=new.z1<cub.z1:
                        z_ranges.append((cub.z0,new.z0-1))
                        z_ranges.append((new.z0,new.z1))
                        z_ranges.append((new.z1+1,cub.z1))
                    #ncnc case
                    elif new.z0<cub.z0<new.z1<cub.z1:
                        z_ranges.append((new.z0,cub.z0-1))
                        z_ranges.append((cub.z0,new.z1))
                        z_ranges.append((new.z1+1,cub.z1))
                    #nccn case
                    elif new.z0<cub.z0<=cub.z1<new.z1:
                        z_ranges.append((new.z0,cub.z0-1))
                        z_ranges.append((cub.z0,cub.z1))
                        z_ranges.append((cub.z1+1,new.z1))
                    else:
                        print('Error, z ranges not found') 

                    #print(x_ranges)
                    #print(y_ranges)
                    #print(z_ranges)
                    for a in x_ranges:
                        for b in y_ranges:
                            for c in z_ranges:
                                sub=Cuboid(a[0],a[1],b[0],b[1],c[0],c[1])
                                #print(sub)
                                if cub.any_overlap(sub) and not new.any_overlap(sub): #Append sub-cuboids if they are part of cub that doesn't overlap new
                                    #print('^Part of cub, not new')
                                    new_cuboids.append(sub)
                else: #If new cuboid doesn't overlap existing cuboid, keep existing cuboid as is
                    new_cuboids.append(cub)
            if type=='on': #If new cuboid is an addition ('on') then add it to the list - existing cuboids have had their overlaps removed so there is no double-counting
                new_cuboids.append(new)
            self.cuboids=new_cuboids #Overwrite self.cuboids with new list
            #print(sum([x.area() for x in self.cuboids]))

        return(sum([x.area() for x in self.cuboids]))


reactor=Reactor(inp)
print(reactor.run_reboot(1))
print(reactor.run_reboot(2))