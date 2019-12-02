#Advent of Code 2015 Day 21
import itertools

player={'HP':100,'Att':0,'Def':0} #HP, Attack, Defence
boss={'HP':109,'Att':8,'Def':2}

def victory(player,boss): #Resolve fight between player and boss
    while True:
        boss['HP']-=max(player['Att']-boss['Def'],1) #At least 1 damage done each turn
        if boss['HP']<=0:
            return(True)
        player['HP']-=max(boss['Att']-player['Def'],1) #At least 1 damage done each turn
        if player['HP']<=0:
            return(False)
 
def victoryPrint(player,boss): #Resolve fight between player and boss
    while True:
        boss['HP']-=max(player['Att']-boss['Def'],1) #At least 1 damage done each turn
        print('Boss: '+str(boss['HP']))
        if boss['HP']<=0:
            return(True)
        player['HP']-=max(boss['Att']-player['Def'],1) #At least 1 damage done each turn
        print('Player: '+str(player['HP']))
        if player['HP']<=0:
            return(False)
        
#a=victory({'HP': 100, 'Att': 5, 'Def': 0},boss)
weapons={'Dagger':{'Cost':8,'Att':4,'Def':0},
'Shortsword':{'Cost':10,'Att':5,'Def':0},
'Warhammer':{'Cost':25,'Att':6,'Def':0},
'Longsword':{'Cost':40,'Att':7,'Def':0},
'Greataxe':{'Cost':74,'Att':8,'Def':0}}

armor={'Nomail':{'Cost':0,'Att':0,'Def':0},
'Leather':{'Cost': 13,'Att':0,'Def':1},
'Chainmail':{'Cost': 31,'Att':0,'Def':2},
'Splintmail':{'Cost': 53,'Att':0,'Def':3},
'Bandedmail':{'Cost': 75,'Att':0,'Def':4},
'Platemail':{'Cost':102,'Att':0,'Def':5}}

rings={'NoneLeft':{'Cost':0,'Att':0,'Def':0},
'NoneRight':{'Cost':0,'Att':0,'Def':0},
'Damage +1 ':{'Cost': 25,'Att':1,'Def':0},
'Damage +2 ':{'Cost': 50,'Att':2,'Def':0},
'Damage +3 ':{'Cost':100,'Att':3,'Def':0},
'Defense +1':{'Cost': 20,'Att':0,'Def':1},
'Defense +2':{'Cost': 40,'Att':0,'Def':2},
'Defense +3':{'Cost': 80,'Att':0,'Def':3}}

def solveA(player,boss,weapons, armor, rings): #Find cheapest equipment required for victory
    minCost=float('inf')
    for wk, w in weapons.items():
        for ak, a in armor.items():
            for rk in itertools.combinations(rings,2):
                r0=rings[rk[0]]
                r1=rings[rk[1]]
                cost=w['Cost']+a['Cost']+r0['Cost']+r1['Cost']
                attSum=player['Att']+w['Att']+r0['Att']+r1['Att']
                defSum=player['Def']+a['Def']+r0['Def']+r1['Def']
                equippedPlayer={'HP':player['HP'],'Att':attSum,'Def':defSum}
                if victory(equippedPlayer,boss.copy()) and cost<minCost:
                    minCost=cost
                    print('Cost: '+str(cost))
                    print(str(equippedPlayer))
                    print(wk+'+'+ak+'+'+rk[0]+'+'+rk[1])
    return(minCost)

#retA=solveA(player,boss,weapons,armor,rings)
                
def solveB(player,boss,weapons, armor, rings): #Find most expensive equipment leading to loss
    maxCost=0
    for wk, w in weapons.items():
        for ak, a in armor.items():
            for rk in itertools.combinations(rings,2):
                r0=rings[rk[0]]
                r1=rings[rk[1]]
                cost=w['Cost']+a['Cost']+r0['Cost']+r1['Cost']
                attSum=player['Att']+w['Att']+r0['Att']+r1['Att']
                defSum=player['Def']+a['Def']+r0['Def']+r1['Def']
                equippedPlayer={'HP':player['HP'],'Att':attSum,'Def':defSum}
                if not victory(equippedPlayer,boss.copy()) and cost>maxCost:
                    maxCost=cost
                    print('Cost: '+str(cost))
                    print(str(equippedPlayer))
                    print(wk+'+'+ak+'+'+rk[0]+'+'+rk[1])
    return(maxCost)

retB=solveB(player,boss,weapons,armor,rings)