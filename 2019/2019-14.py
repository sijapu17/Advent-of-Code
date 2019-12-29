#Advent of Code 2019 Day 14

from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-14.txt')
contents = f.read()
input=contents.splitlines()

def parse(input): #Parse input into recipe dictionary
    recipes={} #Recipe dictionary
    for line in input:
        #Split recipe into inputs and outputs
        recIn=line.split(' => ')[0]
        recOut=line.split(' => ')[1]
        product=recOut.split()[1] #Output product
        quant=int(recOut.split()[0]) #Quantity of products produced
        dictIn={}
        for x in recIn.split(', '):
            dictIn[x.split()[1]]=int(x.split()[0])
        recipes[product]={'ingredients':dictIn,'quantity':quant}
    return(recipes)

recipes=parse(input)

def nextReaction(inventory): #Finds a chemical that needs to be produced, only returning ORE if there is nothing outstanding
    for k,v in inventory.items():
        if k!='ORE' and v>0:
            return(k)
    return('ORE')

def solveA(recipes): #Determine amount of ORE required to produce 1 FUEL, working backwards
    inventory=defaultdict(int) #Positive count represents outstanding chemicals, negative count represents spares
    inventory['FUEL']=1 #Request 1 FUEL
    prod=nextReaction(inventory)
    while prod!='ORE':
        recipe=recipes[prod]
        inventory[prod]-=recipe['quantity'] #Subtract product inventory by recipe quantity
        for k,v in recipe['ingredients'].items(): #Add 
            inventory[k]+=v
        prod=nextReaction(inventory)
    print(str(inventory))
    return(inventory['ORE'])
        
retA=solveA(recipes)        
        