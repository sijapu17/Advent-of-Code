#Advent of Code 2020 Day 7

from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-07.txt')
contents = f.read()
input=contents.splitlines()

class Bags():

    def __init__(self,input): #Parse bag instructions into a tree
        
        self.bagDict=defaultdict(dict)

        for ln in input:
            outer=ln.split(' bags contain')[0]
            words=ln.split() #Split string into words
            inner=dict()
            i=4 #Position of first inner bag record
            if words[4] == 'no': #Do not proceed if there are no inner bags
                self.bagDict[outer]={}
            else:
                while i<len(words):
                    bag=words[i+1]+' '+words[i+2]
                    inner[bag]=int(words[i])
                    i+=4 #Move to next inner bag
                self.bagDict[outer]=inner

    def isColorIn(self,outer,color): #Returns True if inner color is contained in outer bag (at any level)

        if color in self.bagDict[outer]: #If inner is directly in outer then end recursion
            return(True)
        else:
            for inner in self.bagDict[outer]: #Recursively check inner bags
                if self.isColorIn(inner,color):
                    return(True)
            return(False)

    def countContainers(self,color): #Count number of bags that can contain the specified color

        count=0
        for bag in self.bagDict:
            count+=self.isColorIn(bag,color)
        return(count)

    def countContents(self,outer): #Count total number of bags inside a given bag

        count=0
        for k,v in self.bagDict[outer].items(): #Recursively check inner bags
            count+=v #Add immediate inner bags to count
            count+=v*self.countContents(k) #Add contents of inner bags to count
        return(count)


bags=Bags(input)
print(bags.countContainers('shiny gold'))
print(bags.countContents('shiny gold')) #Subtract 1 from this answer as this count includes outermost bag