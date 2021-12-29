#Advent of Code 2021 Day 17
import re, math
inp = 'target area: x=217..240, y=-126..-69'

class Launcher():
    def __init__(self,inp) -> None:
        #Parse target area
        p=re.compile('target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)')
        m=re.match(p,inp)
        self.target_area={}
        self.target_area['x']=(int(m.group(1)),int(m.group(2)))
        self.target_area['y']=(int(m.group(3)),int(m.group(4)))
        #Find minimum x-velocity required to reach target area - total x-reach = v*(v+1)/2
        self.min_v_x=1
        while self.min_v_x*(self.min_v_x+1)/2<self.target_area['x'][0]:
            self.min_v_x+=1
        #Max x-velocity reaches target area in one step
        self.max_v_x=self.target_area['x'][1]
        #Max y-velocity is the vertical distance of bottom of target area from origin
        self.max_v_y=abs(self.target_area['y'][0])
        self.min_v_y=-1*abs(self.target_area['y'][0])

    def run_step(self): #Run 1 step of probe movement
        self.pos[0]+=self.v[0] #Change horizontal position
        self.pos[1]+=self.v[1] #Change vertical position
        if self.v[0]>0: #Horizontal drag
            self.v[0]-=1
        elif self.v[0]<0:
            self.v[0]+=1
        self.v[1]-=1 #Gravity

    def in_target_area(self):
        return(self.target_area['x'][0]<=self.pos[0]<=self.target_area['x'][1] and self.target_area['y'][0]<=self.pos[1]<=self.target_area['y'][1])

    def x_vel_too_low(self):
        return(self.pos[0]<self.target_area['x'][0] and self.v[0]==0)

    def y_vel_too_high(self):
        return(self.pos[0]>self.target_area['x'][1])

    def missed_target(self): #If probe goes past right x-coordinate or bottom y-coordinate of target area then it can never reach it
        return(self.pos[1]<self.target_area['y'][0] or self.y_vel_too_high() or self.x_vel_too_low())

    def find_max_y(self,v): #Runs launch with specified velocity and returns max y position reached
        #Starting position and velocity
        self.v=list(v)
        self.pos=[0,0]
        max_y=0
        while not self.missed_target():
            self.run_step()
            if self.v[1]==0: #Max y-position occurs where y-velocity is 0
                max_y=self.pos[1]
            if self.in_target_area():
                return(max_y)
        return(-math.inf) #If target was missed, don't consider its max y

    def check_hit(self,v): #Runs launch with specified velocity and returns max y position reached
        #Starting position and velocity
        self.v=list(v)
        self.pos=[0,0]
        max_y=0
        while not self.missed_target():
            self.run_step()
            if self.in_target_area():
                return(1)
        return(0)

def find_max_possible_y(launcher): #Loop through possible launches to find highest possible y reached
    max_y=0
    for v_i in range(launcher.min_v_x,launcher.max_v_x+1):
        v_j=1
        while v_j<launcher.max_v_y: #For each x-velocity, loop over different y-velocities
            max_y=max(max_y,launcher.find_max_y((v_i,v_j)))
            if launcher.y_vel_too_high():
                break
            v_j+=1
    return(max_y)

def count_hits(launcher): #Loop through possible launches to find highest possible y reached
    hits=0
    for v_i in range(launcher.min_v_x,launcher.max_v_x+1):
        for v_j in range(launcher.min_v_y,launcher.max_v_y+1): #For each x-velocity, loop over different y-velocities
            hits+=launcher.check_hit((v_i,v_j))
    return(hits)

launcher=Launcher(inp)
print(find_max_possible_y(launcher))
print(count_hits(launcher))