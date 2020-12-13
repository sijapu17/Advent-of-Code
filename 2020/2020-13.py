#Advent of Code 2020 Day 13

from functools import reduce
from datetime import datetime

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-13.txt')
contents = f.read()
input=contents.splitlines()

class Buses1(): #Timetable of buses (Part 1)

    def __init__(self,input):
        self.start=int(input[0]) #Start of waiting time
        self.buses=[] #List of bus numbers
        for b in input[1].split(','):
            if b!='x': #Ignore x for now
                self.buses.append(int(b))

    def find_next_bus(self):
        print(str(self.start))
        best_time=float('inf') #Lowest waiting time so far, initialise at Inf
        best_ID=None #ID of bus with lowest waiting time so far
        for b in self.buses:
            past=self.start%b #Number of minutes past the previous bus
            wait=(b-past)%b
            print('Bus: '+str(b)+' Wait time: '+str(wait))
            if wait<best_time: #Update best time if current bus is better
                best_ID=b
                best_time=wait
        
        return(best_time*best_ID)

buses=Buses1(input)
print(buses.find_next_bus())


class Buses2(): #Timetable of buses (Part 2)

    def __init__(self,input):
        i=0
        self.buses=[] #List of bus numbers and offsets
        for b in input[1].split(','):
            if b!='x':
                bus={}
                bus['period']=int(b) #Bus ID
                bus['offset']=i%bus['period'] #Link bus number to time offset
                self.buses.append(bus)
            i+=1
        self.buses.sort(reverse=True,key=lambda k: k['period']) #Sort bus periods in descending order

    def combine_all_buses(self): #Combine all buses pairwise
        combined=reduce(combine_2_buses,self.buses)
        return(combined['period']-combined['offset'])

def combine_2_buses(b1,b2): #Combine 2 buses into 1 'bus' that matches the period/offset of when the two buses align
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(str(b2))
    t=b1['offset'] #First departure time for b1
    while True: #Increase t by steps of b1's period until t matches b2's period/offset
        if t%b2['period']==b2['offset']:
            break
        t+=b1['period']
    newbus={}
    newbus['period']=b1['period']*b2['period'] #Bus periods are coprime so combined period is product
    newbus['offset']=t%newbus['period'] #Offset is the number of timesteps that t is past the new period
    return(newbus)


buses=Buses2(input)
print(buses.combine_all_buses())