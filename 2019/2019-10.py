#Advent of Code 2019 Day 10ex

from fractions import Fraction
from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-10.txt')
contents = f.read()
input=contents.splitlines()

class Sky(): #Sky full of asteroids

    def __init__(self,input): #Convert input into asteroid list
        self.w=len(input[0])
        self.h=len(input)
        self.astLocs=[] #List of asteroid locations
        for j in range(self.h):
            for i in range(self.w):
                if input[j][i]=='#':
                    self.astLocs.append(complex(i,self.h-1-j)) #Flip y-axis so we can use fractions for correct rotational order
                    
    def __str__(self): #Display map of asteroids
        ret=''
        for j in range(self.h):
            for i in range(self.w):
                if complex(i,self.h-1-j) in self.astLocs: #Un-flip y-axis to print high-to-low
                    ret+='#'
                else:
                    ret+='.'
            ret+='\n'
        return(ret)
                    
sky=Sky(input)

def maxInSight(sky): #Count how many asteroids are in sight of each other asteroid, and find the max
    mx=0
    for ast in sky.astLocs:
        #Calculate bearings from origin asteroid to others - if a group of asteroids share a bearing, they will be seen as one
        bearings=set()
        for oth in sky.astLocs:
            rel=oth-ast
            if rel!=0: #Exclude origin asteroid from list
                if rel.real!=0:
                    bear=str(Fraction(int(rel.imag),int(rel.real)))
                    if rel.real>0: #Use +/- to distinguish between the same bearing on opposite sides of origin
                        bearing='+'+bear
                    elif rel.real<0:
                        bearing='-'+bear
                elif rel.imag>0:
                    bearing='+Inf'
                else:
                    bearing='-Inf'
                bearings.add(bearing)
        if len(bearings)>mx:
            mx=len(bearings)
            bestLoc=ast
    print(mx)
    return(bestLoc)

retA=maxInSight(sky)
          
def astSort(bear): #Sort function for asteroids based on bearing, starting due North and rotating clockwise
    if bear[0]=='R': #On right side, sort North to South
        ret=[0]
    elif bear[0]=='L': #On left side, sort South to North
        ret=[1]
    if bear[1]=='Inf':
        ret.append(-float("inf"))
    else:
        ret.append(-bear[1])
    return(ret)
                
def nthHit(sky,loc,n): #Find the nth asteroid to be hit by the rotating laser at location loc
    mx=0
    ast=loc
    #Calculate bearings from origin asteroid to others - if a group of asteroids share a bearing, they will be seen as one
    bearings=defaultdict(set)
    for oth in sky.astLocs:
        rel=oth-ast
        mag=int(abs(rel)) #Magnitude of asteroid from origin
        if rel!=0: #Exclude origin asteroid from list
            if rel.real!=0: #Define bearing as a tuple of L/R plus the y/x fraction
                bear=Fraction(int(rel.imag),int(rel.real))
                if rel.real>0:
                    bearing=('R',bear)
                elif rel.real<0:
                    bearing=('L',bear)
            elif rel.imag>0:
                bearing=('R','Inf')
            else:
                bearing=('L','Inf')
            bearings[bearing].add((oth,mag)) #For each bearing, store asteroid position and distance from station
    ordered=sorted(bearings,key=astSort)
    candidates=ordered[n-1]
    nth=min(bearings[candidates],key=lambda x:x[1])[0]
    return(complex(nth.real,sky.h-1-nth.imag)) #Flip y-axis to return to decreasing-y

retB=nthHit(sky,retA,200)
        
            
            
            
            
            
            
            
            
            