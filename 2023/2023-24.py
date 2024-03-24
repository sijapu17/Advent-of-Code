#Advent of Code 2023 Day 24

import re
import sympy
from itertools import combinations

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-24.txt')
contents = f.read()
input = contents.splitlines()
p1=re.compile('(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)')

class Hail():
    def __init__(self,line,id) -> None:
        m=p1.match(line)
        self.id=id
        self.p={}
        self.v={}
        #Starting position and velocity
        self.p['x']=int(m.group(1))
        self.p['y']=int(m.group(2))
        self.p['z']=int(m.group(3))
        self.v['x']=int(m.group(4))
        self.v['y']=int(m.group(5))
        self.v['z']=int(m.group(6))
        #Equations
        self.t=sympy.symbols(f't_{self.id}')
        self.x=self.p['x']+self.t*self.v['x']
        self.y=self.p['y']+self.t*self.v['y']
        self.z=self.p['z']+self.t*self.v['z']

    def __str__(self) -> str:
        return(f'H({self.p}, {self.v})')
    
    def __repr__(self) -> str:
        return(self.__str__())
    
hailstones=[Hail(a,n) for n,a in enumerate(input)]

#test_area=(7,27)
test_area=(200000000000000,400000000000000)

def count_xy_collisions():
    collisions=0
    for a, b in combinations(hailstones,2):
        t_sols=sympy.solve([a.x-b.x,a.y-b.y],[a.t,b.t])
        if len(t_sols)>0:
            x_sol=a.x.subs(a.t,t_sols[a.t])
            y_sol=a.y.subs(a.t,t_sols[a.t])
            #print(f'{t_sols} x_sol={float(x_sol)} y_sol={float(y_sol)}')
            if min(x_sol, y_sol)>=test_area[0] and max(x_sol, y_sol)<=test_area[1] and min(t_sols.values())>=0:
                collisions+=1
    return(collisions)
    
#print(count_xy_collisions())

#Part 2

#Rock position at time t = r_p + t * r_v
r_px, r_py, r_pz, r_vx, r_vy, r_vz=sympy.symbols('r_px r_py r_pz r_vx r_vy r_vz')

#Create simultaneous equations for collisions with first 3 hailstones (a, b, c)
a=hailstones[0]
b=hailstones[1]
c=hailstones[2]
t_a, t_b, t_c=sympy.symbols('t_a t_b t_c')

#At time t_a, rock collides with hailstone a
a_x = a.p['x']+(t_a*a.v['x']) - (r_px + (t_a * r_vx))
a_y = a.p['y']+(t_a*a.v['y']) - (r_py + (t_a * r_vy))
a_z = a.p['z']+(t_a*a.v['z']) - (r_pz + (t_a * r_vz))
#At time t_b, rock collides with hailstone b
b_x = b.p['x']+(t_b*b.v['x']) - (r_px + (t_b * r_vx))
b_y = b.p['y']+(t_b*b.v['y']) - (r_py + (t_b * r_vy))
b_z = b.p['z']+(t_b*b.v['z']) - (r_pz + (t_b * r_vz))
#At time t_c, rock collides with hailstone c
c_x = c.p['x']+(t_c*c.v['x']) - (r_px + (t_c * r_vx))
c_y = c.p['y']+(t_c*c.v['y']) - (r_py + (t_c * r_vy))
c_z = c.p['z']+(t_c*c.v['z']) - (r_pz + (t_c * r_vz))

#Solve for unknowns
sols=sympy.solve([a_x, a_y, a_z, b_x, b_y, b_z, c_x, c_y, c_z],[t_a, t_b, t_c, r_px, r_py, r_pz, r_vx, r_vy, r_vz])
print(sols)
print(sum(sols[0][3:6])) #Sum of initial positions