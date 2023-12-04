#Advent of Code 2023 Day 4

import re


f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-04.txt')
contents = f.read()
input = contents.splitlines()

class Card():
    def __init__(self,line) -> None:
        self.id=int(re.search(r"Card\s+(\d+):",line).group(1))
        self.winning_nums=set([int(x) for x in re.findall(r"\d+",line.split(':')[1].split('|')[0])])
        self.nums_i_have=set([int(x) for x in re.findall(r"\d+",line.split(':')[1].split('|')[1])])
        self.overlap=len(self.winning_nums & self.nums_i_have) #Number of matches

    def get_score(self):
        if self.overlap>0:
            return(2**(self.overlap-1))
        return(0)

#Parse cards
cards={}
for line in input:
    card=Card(line)
    cards[card.id]=card

def total_score():
    return(sum([c.get_score() for c in cards.values()]))

def count_cards():
    #Initialise card index with 1 of each card
    card_index={}
    for i in range(1,len(cards)+1):
        card_index[i]=1
    #Loop through cards, adding copies of future cards
    for i in range(1,len(cards)+1):
        n=card_index[i] #Number of current card ID
        for j in range(cards[i].overlap):
            card_index[i+j+1]+=n #Add n copies of the next j cards
    return(sum([x for x in card_index.values()]))

print(total_score())
print(count_cards())
