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

def oreForNFuel(recipes,n): #Determine amount of ORE required to produce n FUEL, working backwards
    inventory=defaultdict(int) #Positive count represents outstanding chemicals, negative count represents spares
    inventory['FUEL']=n #Request 1 FUEL
    prod=nextReaction(inventory)
    while prod!='ORE':
        recipe=recipes[prod]
        mult=(inventory[prod] + (recipe['quantity']-1)) // recipe['quantity'] #Number of times to run the recipe so prod inventory is 0 or lower
        inventory[prod]-=(mult*recipe['quantity']) #Subtract product inventory by quantity of products produced
        for k,v in recipe['ingredients'].items(): #Add ingredients used to product inventory
            inventory[k]+=(mult*v)
        prod=nextReaction(inventory)
    return(inventory['ORE'])
        
retA=oreForNFuel(recipes,1)

def fuelForTrillionOre(recipes): #Determine amount of fuel that can be produced from 1 trillion ore, using binary search
    trillion=1000000000000 #1 trillion
    lBound=trillion//oreForNFuel(recipes,1) #At least this much fuel can be produced by repeating the 1-fuel process, but this leaves many leftovers
    uBound=lBound*2
    while True:
        if oreForNFuel(recipes,uBound)<trillion: #If upper bound is too low, double it and try again
            uBound*=2
        else:
            break        
    while lBound+1<uBound: #Once range is established, test the midpoint and then halve the range until only two values remain
        print('Range: ('+str(lBound)+', '+str(uBound)+')')
        mid=(lBound+uBound)//2
        ore=oreForNFuel(recipes,mid)
        print(str(mid)+' fuel from '+str(ore)+' ore')
        if ore>trillion: #If more than a trillion ore required to produce fuel, set upper bound to midpoint
            uBound=mid
        elif ore<=trillion: #If less than a trillion ore required to produce fuel, set lower bound to midpoint
            lBound=mid
    #Test final 2 values to find which is correct
    print('Range: ('+str(lBound)+', '+str(uBound)+')')
    lOre=oreForNFuel(recipes,lBound)
    uOre=oreForNFuel(recipes,uBound)
    print(str(lBound)+' fuel from '+str(lOre)+' ore')
    print(str(uBound)+' fuel from '+str(uOre)+' ore')
    if uOre>trillion: #Test whether upper bound is past a trillion or not
        return(lBound)
    else:
        return(uBound)
             
retB=fuelForTrillionOre(recipes)