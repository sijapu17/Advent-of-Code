#Advent of Code 2015 Day 22
import copy

class Fight():
    
    def __init__(self):
        self.boss={'HP':51,'Att':9,'Def':0}
        self.player={'HP':50,'Att':0,'Def':0,'Mana':500}
        #self.boss={'HP':13,'Att':8,'Def':0}
        #self.player={'HP':10,'Att':0,'Def':0,'Mana':250}
        self.mana={'MagicMissile':53,'Drain':73,'Shield':113,'Poison':173,'Recharge':229}
        self.totalMana=0
        self.effectTime={'MagicMissile':0,'Drain':0,'Shield':0,'Poison':0,'Recharge':0}
        self.nextSpell='' #Next spell for player to cast
        self.spellLog='' #Log of all spells cast
        self.status='Ongoing'
        
    def makeCopy(self,spell): #Create copy of fight with a new next move
        new=copy.deepcopy(self)
        new.nextSpell=spell
        if new.spellLog=='':
            new.spellLog=spell
        else:
            new.spellLog+=', '+spell
        return(new)
        
    def resolveEffects(self):
        if self.effectTime['Shield']>0:
            self.player['Def']=7
        if self.effectTime['Poison']>0:
            self.boss['HP']-=3
        if self.effectTime['Recharge']>0:
            self.player['Mana']+=101
        for each in self.effectTime:
            self.effectTime[each]=max(self.effectTime[each]-1,0)
        if self.effectTime['Shield']==0: #Remove shield if it has run out
            self.player['Def']=0
        
    def playerAttack(self,spell):
        self.resolveEffects()
        self.player['Mana']-=self.mana[spell]
        self.totalMana+=self.mana[spell]
        #print('Player casts '+spell)
        if spell=='MagicMissile':
            self.boss['HP']-=4
        elif spell=='Drain':
            self.boss['HP']-=2
            self.player['HP']+=2
        elif spell=='Shield':
            self.effectTime[spell]=6
        elif spell=='Poison':
            self.effectTime[spell]=6
        elif spell=='Recharge':
            self.effectTime[spell]=5
        self.status=self.resultCheck()
        if self.status=='Victory':
            return(self.status)
            
    def bossAttack(self):
        self.resolveEffects()
        self.resultCheck()
        if self.status=='Victory':
            return(self.status)
        #print('Boss attacks')
        self.player['HP']-=max(self.boss['Att']-self.player['Def'],1)
        self.resultCheck()
        if self.status=='Defeat':
            return(self.status)
            
    def resultCheck(self):
        if self.boss['HP']<=0:
            print('Player wins, used '+str(self.totalMana)+' mana')
            print(self.spellLog)
            self.status='Victory'
            return(self.status)
        elif self.player['HP']<=0:
            print('Boss wins')
            self.status='Defeat'
            return(self.status)
        else:
            return('Ongoing')
            
    def runTurns(self,spell): #Run player turn followed by boss turn
        self.playerAttack(spell)
        if self.status!='Ongoing':
            return(self.status)
        self.bossAttack()
        return(self.status)
        
        
def fightA():
    spells=['Drain','Recharge','Shield','MagicMissile','Poison']
    stack=[]
    initial=Fight()
    minMana=float('inf') #Lowest mana spent for a victory
    best=None #Best fight
    for s in spells:
        stack.append(initial.makeCopy(s)) #Try each spell as first spell
    while len(stack)>0:
        print('Stack ('+str(len(stack))+')')
        #for st in stack:
        #    print(st.spellLog)
        candidate=stack.pop()
        if candidate.totalMana<minMana:
            print('Current mana: '+str(candidate.totalMana)+', Best: '+str(minMana))
            candidate.runTurns(candidate.nextSpell)
            if candidate.status=='Victory':
                if candidate.totalMana<minMana:
                    print('New best found: '+str(candidate.totalMana))
                    minMana=candidate.totalMana
                    best=candidate
            elif candidate.status=='Ongoing' and candidate.totalMana<minMana:
                for s in spells:
                    if candidate.player['Mana']>=candidate.mana[s] and candidate.effectTime[s]==0:
                        stack.append(candidate.makeCopy(s))
    #print(best.spellLog)
    return(minMana)
                
retA=fightA()        

"""    
Magic Missile costs 53 mana. It instantly does 4 damage.
Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor's increased by 7.
Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active,
it deals the boss 3 damage.
Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active,
it gives you 101 new mana.
"""