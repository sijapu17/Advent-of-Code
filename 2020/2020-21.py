#Advent of Code 2020 Day 21

from functools import reduce

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-21.txt')
state = f.read()
input=state.splitlines()

class Food(): #List of ingredients and allergens

    def __init__(self,line): #Parse input line into ingredients and allergens
        #Ingredients
        self.ingredients=set(line.split('(contains ')[0].split())
        self.allergens=set(line.split('(contains ')[1].replace(')','').split(', '))
        pass

class Menu():

    def __init__(self,input):
        self.food_list=[]
        for x in input: #Create Food items
            self.food_list.append(Food(x))
        self.all_ingredients=reduce(lambda a,b: a|b,[x.ingredients for x in self.food_list]) #Set of all ingredients on menu
        self.all_allergens=reduce(lambda a,b: a|b,[x.allergens for x in self.food_list]) #Set of all allergens on menu
        self.ing_all_possibilities={}
        for i in self.all_ingredients:
            self.ing_all_possibilities[i]=self.all_allergens.copy()

 #An ingredient cannot contain an allergen if every allergen appears in a food without the ingredient       
    def count_nonallergenic_ingredients(self):

        self.nonallergenic_ingredients=set() #Ingredients which cannot contain an allergen
        for i in self.all_ingredients:
            excluded_allergens=set()
            for a in self.all_allergens:
                for f in self.food_list:
                    if a in f.allergens and i not in f.ingredients:
                        excluded_allergens.add(a)
                        #print(i+' does not contain '+a)
            if excluded_allergens==self.all_allergens:
                self.nonallergenic_ingredients.add(i)
        
        #Count occurrences of non-allergenic ingredients in menu
        count=0
        for f in self.food_list:
            for i in f.ingredients:
                if i in self.nonallergenic_ingredients:
                    count+=1

        return(count)

    def match_allergens(self):
        #Reduce possibile pairs by checking all allergens and ingredients
        for i in self.all_ingredients:
            for a in self.all_allergens:
                for f in self.food_list:
                    if a in f.allergens and i not in f.ingredients:
                        if a in self.ing_all_possibilities[i]:
                            self.ing_all_possibilities[i].remove(a)

        #Remove non-allergens
        self.ing_all_possibilities={k: v for k, v in self.ing_all_possibilities.items() if len(v)>0}
        #Pair off remaining ingredients and allergens
        pairs=[]
        while len(self.ing_all_possibilities)>0:
            ing=min(self.ing_all_possibilities, key=lambda x: len(self.ing_all_possibilities[x])) #Pop an ingredient with only one possible allergen
            alr=self.ing_all_possibilities[ing].pop()
            pair=(ing,alr)
            print(pair)
            pairs.append(pair)
            #Remove matched allergen from other ingredients
            del self.ing_all_possibilities[ing]
            for v in self.ing_all_possibilities.values():
                if alr in v:
                    v.remove(alr) 
        #Sort pairs alphabetically by allergen
        pairs.sort(key=lambda x:x[1])
        ret=','.join([x[0] for x in pairs])
        print(ret)

menu=Menu(input)
print(menu.count_nonallergenic_ingredients())
menu.match_allergens()