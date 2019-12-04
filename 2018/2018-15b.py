#Advent of Code 2018 Day 15

import math
from collections import deque
import string
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-15exMike.txt')
contents = f.read()
input=contents.splitlines()

class Cave(): #Overall class for cave containing map and units
    
    def __init__(self,input,power): #Convert input into map and units
        self.map={}
        self.units={}
        self.w=len(input[0])
        self.h=len(input)
        self.rounds=-1 #Increment number of completed rounds at the start of each round
        self.occupiedCoords=set() #Keep track of which spots are occupied by carts
        self.endOfBattle=False #Change to true when a unit finds no living enemies
        self.checksum=None
        self.deadElf=False #If an elf dies, abort the attempt
        
        lowList=string.ascii_lowercase #Incremental elf ID
        elfI=0
        hiList=string.ascii_uppercase #Incremental goblin ID
        goblinI=0
        
        for j in range(self.h):
            for i in range(self.w):
                x=input[j][i]
                pos=complex(i,j)
                if x in ('E','G'):
                    self.map[pos]='.' #Add in floor hidden by unit
                    self.occupiedCoords.add(pos)
                    if x=='E':
                        id=lowList[elfI] #Assign next lowercase letter to elf
                        self.units[id]=Elf(self,id,pos,power)
                        elfI+=1
                    elif x=='G':
                        id=hiList[goblinI] #Assign next lowercase letter to elf
                        self.units[id]=Goblin(self,id,pos,3)
                        goblinI+=1
                else:
                    self.map[pos]=x

    def unitIDFromPos(self,pos): #Return unit ID given pos
        for k, v in self.units.items():
            if v.alive and v.pos == pos:
                return(k)
        
    def __str__(self):
        ret1='  '
        ret2='  '
        ret3=''
        for i in range(self.w):
            if i%10==0: #Create tens row at top
                ret1+=str(math.floor(abs(i)/10%10))
            else:
                ret1+=' '
            ret2+=str(abs(i)%10) #Create units row at top
        for j in range(self.h):
            if j%10==0:
                ret3+=str(math.floor(abs(j)/10%10)) #Create tens column going down
            else:
                ret3+=' '
            ret3+=str(abs(j)%10) #Create units column going down
            unitsInRow=[] #Collect a list of any units in the row
            for i in range(self.w):
                pos=complex(i,j)
                if pos in self.occupiedCoords:
                    id=self.unitIDFromPos(pos) #Find unit in position
                    symbol=self.units[id].symbol
                    unitsInRow.append(self.units[id])
                    ret3+=symbol
                else:
                    ret3+=self.map[pos]
            if len(unitsInRow)>0: #Print any units in row
                unitDisplay=', '.join([str(x) for x in unitsInRow])
                ret3+='  '+unitDisplay
            ret3+='\n'
        return(ret1+'\n'+ret2+'\n'+ret3)
    
    def initRound(self): #Reset list of units to start round
        self.rounds+=1
        #Sort units by position in reading order, reversed so the next unit can be popped off the end
        coordOrder=sorted(self.occupiedCoords, key = lambda x : (x.imag,x.real), reverse=True)
        self.unitOrder=[self.unitIDFromPos(x) for x in coordOrder]
            
    def getNextUnit(self): #Yield the next unit to move
        while len(self.unitOrder)>0:
            unit=self.units[self.unitOrder.pop()]
            if unit.alive:
                return(unit)
            
    def runRound(self): #Run a round of the battle
        self.initRound() #Initialise round state
        #Carry on round while there are live units yet to move
        while len([x for x in self.unitOrder if self.units[x].alive])>0:
            if self.endOfBattle:
                return(self.checksum)
            unit=self.getNextUnit()
            unit.takeTurn()
            
    def sumHP(self): #Return sum of HP of all units
        sum=0
        for u in [x for x in self.units if self.units[x].alive]:
            sum+=self.units[u].hp
        return(sum)


class Unit(): #Parent class for a unit, which will be either an Elf or a Goblin
    
    def __init__(self,cave,id,pos,power):
        self.cave=cave
        self.id=id
        self.pos=pos
        self.hp=200
        self.power=power #Attack power
        self.alive=True
        self.orthog=[complex(0,-1),complex(-1,0),complex(1,0),complex(0,1)] #Always try to move in order ULRD
        
    def __str__(self):
        return(str(self.id)+'('+str(self.hp)+')')
    
    def takeTurn(self): #First move if able, then attack if in range
        #print("{0} {1} takes a turn".format(self.species, self.id))
        e=self.getEnemies()
        if len(e)==0:
            sumHP=self.cave.sumHP()
            rounds=self.cave.rounds
            checksum=sumHP*rounds
            self.cave.checksum=checksum
            print('End of battle: '+self.species+' victory after '+str(rounds)+' completed rounds')
            print('Outcome= {0} rounds x {1} HP ={2}'.format(str(rounds),str(sumHP),str(checksum)))
            self.cave.endOfBattle=True
        d=self.getDestinations(e)
        newPos=self.getStep(d) #Determine position to move to
        self.move(newPos)
        target=self.getTarget() #Find target to attack, if one exists
        if target is not None:
            #print("{0} {1} targets {2} {3}".format(self.species, self.id, target.species, target.id))
            self.attack(target)
                                        
    
    def isEnemy(self,other): #Determine whether units are enemies, based on species
        if self.species==other.species:
            return(False)
        return(True)
    
    def getEnemies(self): #Create a set of all enemy units in the cave
        enemies=set([self.cave.units[x] for x in self.cave.units if self.cave.units[x].alive and self.isEnemy(self.cave.units[x])])
        return(enemies)
    
    def getDestinations(self,enemies): #Create a set of all destinations adjacent to an enemy
        dests=set()
        for e in enemies:
            ePos=e.pos
            for o in self.orthog:
                dPos=ePos+o
                if self.cave.map[dPos]=='.' and (dPos not in self.cave.occupiedCoords or dPos==self.pos):
                    dests.add(dPos)
        return(dests)
    
    def getStep(self,dests): #Find the step which will move unit to nearest destination, in reading order preference
        pos=self.pos
        if pos in dests:
            return(pos) #If unit is already next to an enemy, stay put
        obstacles=self.cave.occupiedCoords.copy() #Create set of walls and other units which cannot be pathed through
        for k,v in self.cave.map.items():
            if v=='#':
                obstacles.add(k) #Add walls to obstacles
        node={'pos':pos,'path':[],'len':0}
        queue=deque([node])
        visited=set() #If position has already been visited, new path is behind it in reading order
        foundLen=float('Inf') #Track the shortest path to a destination found
        found=[] #Record found paths
        while len(queue)>0:
            node=queue.pop()
            #print(str(node))
            newPath=list(node['path'])
            newPath.append(node['pos']) #Add current position to path
            newLen=node['len']+1
            if newLen>foundLen: #If path is longer than a found path, terminate search
                break
            if node['pos'] in dests:
                found.append(node) #If path is found, add it to found list
                foundLen=newLen
            for o in self.orthog:
                newPos=node['pos']+o
                if newPos not in obstacles: #If new position is unoccupied and unvisited, add to end of queue
                    if newPos not in visited:
                        visited.add(newPos)
                        newNode={'pos':newPos,'path':newPath,'len':newLen}
                        queue.appendleft(newNode)
        if len(found)>0:
            #Sort by reading order of destination, then reading order of first step
            std=sorted(found,key=lambda x : (x['pos'].imag,x['pos'].real))
            #print(std)
            best=std[0]
            if best['len']==1:
                step=best['pos']
            else:
                step=best['path'][1]
            return(step)
        
        #print('No destinations reachable')            
        return(pos) #If no destinations are reachable, stay put
    
    def move(self,newPos): #Move unit to new position, updating Cave.occupiedCoords
        if self.pos!=newPos:
            self.cave.occupiedCoords.remove(self.pos)
            self.pos=newPos
            self.cave.occupiedCoords.add(self.pos)
    
    def getTarget(self): #Find adjacent enemy to attack
        adjacentEnemies=[]
        for o in self.orthog:
            if self.pos+o in self.cave.occupiedCoords: #Check for adjacent units
                if self.isEnemy(self.cave.units[self.cave.unitIDFromPos(self.pos+o)]): #If adjacent unit is enemy
                    adjacentEnemies.append(self.cave.units[self.cave.unitIDFromPos(self.pos+o)]) #then add to list
        if len(adjacentEnemies)>0: #Attack if next to an enemy
            std=sorted(adjacentEnemies, key=lambda x : x.hp) #Find lowest HP, maintaining reading order in ties
            target=std[0]
            return(target)
        return(None)
            
    def attack(self,other): #Attack opposing unit, reducing target HP by own power, killing them if they hit 0HP
        other.hp-=self.power
        #print("{0} {1} attacks {2} {3}".format(self.species, self.id, other.species, other.id))
        if other.hp<=0: #Opponent dies if HP reaches 0
            other.die()
            
    def die(self): #Die, setting status to dead and removing self from Cave.occupiedCoords
        self.alive=False
        self.cave.occupiedCoords.remove(self.pos)
        
        
class Elf(Unit): #Child class for an Elf unit
    
    def __init__(self,cave,id,pos,power):
        super().__init__(cave,id,pos,power)
        self.symbol='E'
        self.species='Elf'
        
    def die(self):
        super().die()
        self.cave.deadElf=True

class Goblin(Unit): #Child class for a Goblin unit
    
    def __init__(self,cave,id,pos,power):
        super().__init__(cave,id,pos,power)
        self.symbol='G'
        self.species='Goblin'
  
#input=['#######','#G...E#','#######']
  
def solveB(input): #Find round where combat ends
    power=4
    while True:        
        cave=Cave(input,power)
        #print(cave)
        while not cave.endOfBattle and not cave.deadElf:
            nRounds=cave.runRound()
            print('Power='+str(power)+' Round '+str(cave.rounds))
            print(cave)
        if not cave.deadElf:
            return(nRounds)
        power+=1


retB=solveB(input)
    
