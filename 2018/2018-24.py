#Advent of Code 2018 Day 24

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-24.txt')
input = f.read().splitlines()
import re

class Battle():
    def __init__(self,input,boost=0):
        p1=re.compile('([\w| ]+):')
        p2=re.compile('(\d+) units each with (\d+) hit points\s?\(?(?:(weak|immune) to ([\w| |,]+))?(?:;\s)?(?:(weak|immune) to ([\w| |,]+))?\)? with an attack that does (\d+) (\w+) damage at initiative (\d+)')
        force=None
        self.groups={}
        self.elapsed=0
        self.unitsLost=1 #Start on 1 so battle doesnt stop before first round
        #Debugging - set min and max rounds to print
        self.minRound=98050
        self.maxRound=98050
        for line in input:
            if p1.match(line):
                m1=p1.match(line)
                force=m1.group(1)
            elif p2.match(line):
                m2=p2.match(line)
                nUnits=int(m2.group(1))
                HP=int(m2.group(2))
                weakID=immID=None
                if m2.group(3)=='weak':
                    weakID=4
                elif m2.group(3)=='immune':
                    immID=4
                if m2.group(5)=='weak':
                    weakID=6
                elif m2.group(5)=='immune':
                    immID=6
                if weakID is not None:
                    weaks=set(m2.group(weakID).split(', '))
                else:
                    weaks=set()
                if immID is not None:
                    imms=set(m2.group(immID).split(', '))
                else:
                    imms=set()
                attack=int(m2.group(7))
                if force=='Immune System':
                    attack+=boost
                attType=m2.group(8)
                initiative=int(m2.group(9))
                self.groups[initiative]=Group(self,force,nUnits,HP,imms,weaks,attack,attType,initiative)
            elif len(line)>0:
                print('No match for: '+str(line))

    def __str__(self):
        ret='\nRound '+str(self.elapsed)+':\n'
        for g in self.groups.values():
            if g.alive:
                ret+=str(g)+' contains '+str(g.nUnits)+' units\n'
        return(ret)

    def nGroups(self,force): #Count number of live groups for given force
        return(len([x for x in self.groups.values() if x.force==force and x.alive]))
    
    def ongoing(self): #Check whether battle is still ongoing (i.e. if both forces still have live groups
        return(min(self.nGroups('Immune System'),self.nGroups('Infection'))>0 and self.unitsLost>0)
    
    def victory(self): #Check for immune system victory
        if self.nGroups('Immune System')>0 and self.nGroups('Infection')==0:
            return(True)
        return(False)
    
    def totalUnits(self): #Count total remaining units across all groups
        return(sum([x.nUnits for x in self.groups.values() if x.alive]))

    def resetTargets(self):
        self.unitsLost=0
        for g in self.groups.values():
            g.targetID=None
            g.targetedID=None
                
    def targetingOrder(self):
        groups=sorted(list(self.groups.values()),key=lambda x:(x.effectivePower(),x.initiative),reverse=True)
        live=[x for x in groups if x.alive] #Dead units cannot target
        return(live)
    
    def targetPhase(self):
        order=self.targetingOrder()
        if self.minRound<=self.elapsed<=self.maxRound:
            print('Target order: '+str(order))
        for o in order:
            o.chooseTarget()
        
    def attackingOrder(self):
        groups=sorted(list(self.groups.values()),key=lambda x:x.initiative,reverse=True)
        live=[x for x in groups if x.targetID is not None] #Only units with a target can attack
        return(live)
    
    def attackPhase(self):
        order=self.attackingOrder()
        if self.minRound<=self.elapsed<=self.maxRound:
            print('Attack order: '+str(order))
        for o in order:
            o.attackTarget()
            

    def runRound(self):
        self.resetTargets()
        self.targetPhase()
        self.attackPhase()
        self.elapsed+=1

class Group(): #Group of fighting units
    def __init__(self,battle,force,nUnits,HP,imms,weaks,attack,attType,initiative):
        self.battle=battle
        self.force,self.nUnits,self.HP,self.imms,self.weaks,self.attack,self.attType,self.initiative=force,nUnits,HP,imms,weaks,attack,attType,initiative
        self.alive=True
        self.targetID=None
        self.targetedID=None
        
    def __str__(self):
        return(self.force+' #'+str(self.initiative))
    
    def details(self):
        ret=str(self)+' '+str(self.nUnits)+' units of '+str(self.HP)+'HP (I:'+str(self.imms)+',W:'+str(self.weaks)+') '+str(self.attack)+' '+self.attType+' attack\nStatus: '
        if self.alive:
            ret+='Alive'
        else:
            ret+='Dead'
        ret+='Targeting #'+str(self.targetID)+', targeted by #'+str(self.targetedID)
        print(ret)
    
    def __repr__(self):
        return(self.__str__())
    
    def isEnemy(self,other):
        return(self.force!=other.force)
    
    def effectivePower(self):
        return(self.nUnits*self.attack)
    
    def chooseTarget(self):
        candidates=[x for x in self.battle.groups.values() if x.alive and x.targetedID==None and self.isEnemy(x)]
        if len(candidates)>0:
            sort={} #Dictionary to sort candidates by damage, enemy EP and initiative
            for c in candidates:
                mult=1
                if self.attType in c.weaks:
                    mult=2
                elif self.attType in c.imms: #Do not target immune groups
                    continue
                sort[c.initiative]=(mult,c.effectivePower(),c.initiative)
            if len(sort)>0:
                self.targetID=max(sort,key=lambda x:sort[x]) #Assign target to group
                target=self.battle.groups[self.targetID]
                target.targetedID=self.initiative #Mark target so they cannot be targeted again
                if self.battle.minRound<=self.battle.elapsed<=self.battle.maxRound:
                    print('Round '+str(self.battle.elapsed)+': '+str(self)+' targets '+str(target))
            
    def attackTarget(self): #Attack the targeted group
        if self.alive:
            target=self.battle.groups[self.targetID]
            mult=1
            if self.attType in target.weaks:
                mult=2
            elif self.attType in target.imms:
                mult=0
            damage=self.effectivePower()*mult
            unitsLost=min(damage//target.HP,target.nUnits)
            self.battle.unitsLost+=unitsLost #Check for stalemates
            target.nUnits-=unitsLost
            if self.battle.minRound<=self.battle.elapsed<=self.battle.maxRound:
                print('Round '+str(self.battle.elapsed)+': '+str(self)+' attacks '+str(target)+', killing '+str(unitsLost)+' units')
            if target.nUnits<=0:
                target.alive=False
                #print('Round '+str(self.battle.elapsed)+': '+str(target)+' dies')
                    

def solveA(input):
    battle=Battle(input)
    while battle.ongoing():# and battle.elapsed<2:
        battle.runRound()
        if battle.elapsed%100==1:
            print(battle)
    return(battle.totalUnits())
    
#retA=solveA(input)

def solveB(input):
    boost=1
    while True:
        battle=Battle(input,boost)
        print('Boost='+str(boost))
        while battle.ongoing():# and battle.elapsed<2:
            battle.runRound()
            #if battle.elapsed%100==1:
            #    print(battle)
        print(battle)
        if battle.victory():
            return(battle.totalUnits())
        boost+=1

retB=solveB(input)