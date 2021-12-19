#Advent of Code 2021 Day 14
from collections import Counter
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-14.txt')
contents = f.read()
inp = contents.splitlines()

class Polymer():
    def __init__(self,inp):
        polymer=inp[0]
        self.end_element=polymer[-1]
        self.recipe={} #Dict mapping each pair to their insertion letter
        for l in inp[2:]:
            self.recipe[l.split(' -> ')[0]]=l.split(' -> ')[1]
        self.pairs=Counter() #Count number of occurences of each pair in the polymer
        for i in range(len(polymer)-1):
            self.pairs[polymer[i:i+2]]+=1

    def __str__(self) -> str:
        return(str(self.pairs))

    def count_elements(self): #Count all elements in current polymer
        element_count=Counter()
        for k,v in self.pairs.items():
            element_count[k[0]]+=v
        element_count.update(self.end_element) #Count of elements misses out last element as it is not the start of a pair, so add in to correct this
        print(element_count)
        #Return the count of the most common element minus the count of the least common element
        least_count=min([x for x in element_count.values()])
        most_count=max([x for x in element_count.values()])
        return(most_count-least_count)
    
    def run_step(self):
        new_pairs=Counter()
        for k,v in self.pairs.items(): #k = element pair, v = number of occurrences of pair
            element=self.recipe[k] #Element to insert between pair
            new_pairs[k[0]+element]+=v #Create v new front pairs
            new_pairs[element+k[1]]+=v #Create v new back pairs
        self.pairs=new_pairs #Replace existing pairs with new ones

    def run_n_steps(self,n):
        for i in range(n):
            self.run_step()

polymer=Polymer(inp)
print(polymer)
polymer.run_n_steps(40)
print(polymer.count_elements())
