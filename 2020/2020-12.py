#Advent of Code 2020 Day 12

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-12.txt')
state = f.read()
input=state.splitlines()

class Ship(): #Ship to run navigation actions

    def __init__(self,input):

        self.actions=[] #List of actions
        for x in input: #Parse input into list of actions
            a=dict()
            a['act']=x[0] #Action
            a['val']=int(x[1:]) #Value of action
            self.actions.append(a)

        self.pos=0j #Starting position
        self.dir=1+0j #Starting direction (East)
        self.way=complex(10,1) #Starting position of waypoint (relative to ship)

    def run_action(self,action): #Run a single action using part 1 action definitions

        #Move position in given direction while not changing ship direction
        if action['act']=='N':
            self.pos+=complex(0,action['val'])
        elif action['act']=='S':
            self.pos-=complex(0,action['val'])
        elif action['act']=='E':
            self.pos+=complex(action['val'],0)
        elif action['act']=='W':
            self.pos-=complex(action['val'],0)
        #Rotate ship
        elif action['act']=='L':
            r=action['val']//90 #Convert degrees to number of 90-degree rotations
            self.dir*=complex(0,1)**r #Rotate left by multiplying by i r times
        elif action['act']=='R':
            r=action['val']//90 #Convert degrees to number of 90-degree rotations
            self.dir*=complex(0,-1)**r #Rotate right by multiplying by -i r times
        #Move forward in curent direction
        elif action['act']=='F':
            self.pos+=self.dir*action['val']

    def run_action_way(self,action): #Run a single action using part 2 (waypoint) action definitions

        #Move waypoint in given direction
        if action['act']=='N':
            self.way+=complex(0,action['val'])
        elif action['act']=='S':
            self.way-=complex(0,action['val'])
        elif action['act']=='E':
            self.way+=complex(action['val'],0)
        elif action['act']=='W':
            self.way-=complex(action['val'],0)
        #Rotate waypoint
        elif action['act']=='L':
            r=action['val']//90 #Convert degrees to number of 90-degree rotations
            self.way*=complex(0,1)**r #Rotate left by multiplying by i r times
        elif action['act']=='R':
            r=action['val']//90 #Convert degrees to number of 90-degree rotations
            self.way*=complex(0,-1)**r #Rotate right by multiplying by -i r times
        #Move forward in direction of waypoint
        elif action['act']=='F':
            self.pos+=self.way*action['val']

    def manhatten(self): #Return Manhatten distance of current position from origin
        return(int(abs(self.pos.real)+abs(self.pos.imag)))

    def status(self): #Print current position and direction
        ret='Pos: {0} Dir: {1} Dist: {2}'.format(self.pos,self.dir,self.manhatten())
        print(ret)

    def status_way(self): #Print current position and waypoint position
        ret='Pos: {0} Way: {1} Dist: {2}'.format(self.pos,self.way,self.manhatten())
        print(ret)

    def run_all_actions(self): #Run all actions and report Manhatten distance of final position
        
        for a in self.actions:
            self.run_action(a)

        return(self.manhatten())

    def run_all_actions_way(self): #Run all actions and report Manhatten distance of final position
        
        for a in self.actions:
            self.run_action_way(a)

        return(self.manhatten())

ship=Ship(input)
print(ship.run_all_actions()) #Part 1
ship=Ship(input)
print(ship.run_all_actions_way()) #Part 2