#Advent of Code 2022 Day 15

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-15.txt')
contents = f.read()
inp = contents.splitlines()

def man_dist(c1:complex,c2:complex): #Return Manhatten Distance
    return(abs(c1.real-c2.real)+abs(c1.imag-c2.imag))

class System():
    def __init__(self,inp,bound) -> None:
        
        self.bound=bound
        self.sensors=[]
        for line in inp:
            d=re.findall(r"-?\d+", line) #Collect all digits
            self.sensors.append(Sensor(complex(int(d[0]),int(d[1])),complex(int(d[2]),int(d[3]))))

    def count_empties_row(self,y): #Count confirmed empty spaces in row y
        empties=set() #Set of confirmed empty coords
        for s in self.sensors:
            intercept=complex(s.pos.real,y) #Closest point to sensor on row y
            j=man_dist(s.pos,intercept) #Vertical distance from sensor to row y
            i=0
            while i+j<=s.range: #Add all points on row y within range
                empties.add(intercept+complex(i,0))
                empties.add(intercept-complex(i,0))
                i+=1
            if s.beacon in empties:
                empties.remove(s.beacon)
        return(len(empties))
    
    def find_empty(self): #Find the coord not covered by any sensor
        latest=self.sensors[0] #Initialise to an arbitrary sensor
        n=0 #Count of sensors
        for s in self.sensors: #Loop through sensors
            n+=1
            print(f'Checking sensor {n} of {len(self.sensors)}')
            for b in s.border(): #Loop through coords in border of sensor
                if 0<=b.real<=self.bound and 0<=b.imag<=self.bound: #Check if b is in bounds
                    in_range=False #Initialise flag
                    if latest.in_range(b): #Check latest sensor first, as this will usually be in range
                        in_range=True
                        continue
                    for o in self.sensors: #Loop through other sensors
                        if o.in_range(b):
                            latest=o
                            in_range=True
                            break
                    if not in_range: #If b is not in range of any sensor, it is the answer
                        print(b)
                        return(int(4000000*b.real+b.imag))
                        

class Sensor(): #Individual sensor
    def __init__(self,pos:complex,beacon:complex) -> None:
        self.pos=pos
        self.beacon=beacon
        #Distance from sensor where there are no other beacons
        self.range=man_dist(pos,beacon)

    def __str__(self) -> str:
        return(f'{self.pos} --{self.range}-> {self.beacon}')
    
    def __repr__(self) -> str:
        return(self.__str__())
    
    def in_range(self,p) -> bool:
        return(man_dist(self.pos,p)<=self.range)
    
    def border(self): #Sequentially generate coordinates 1 space outside of sensor range
        b_pos=self.pos+complex(0,self.range+1) #Start at top of range diamond
        for d in (complex(1,-1),complex(-1,-1),complex(-1,1),complex(1,1)):
            while True:
                b_pos+=d
                yield(b_pos)
                if b_pos.real==self.pos.real or b_pos.imag==self.pos.imag:
                    break

system=System(inp,4000000)
print(system.count_empties_row(2000000))
print(system.find_empty())