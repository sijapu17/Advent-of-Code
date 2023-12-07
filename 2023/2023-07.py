#Advent of Code 2023 Day 7
from collections import Counter

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-07.txt')
contents = f.read()
input = contents.splitlines()

class Hand():
    def __init__(self,s) -> None:
        self.s=s
        counter=Counter(s) #Convert string into Counter object
        #Work out what type of hand
        mx=max(counter.values())
        match mx:
            case 5:
                rank=7 #5 of a kind
            case 4:
                rank=6 #4 of a kind
            case 3:
                if 2 in counter.values():
                    rank=5 #Full House
                else:
                    rank=4 #3 of a kind
            case 2:
                if len([x for x in counter.values() if x==2])==2:
                    rank=3 #2 pair
                else:
                    rank=2 #1 pair
            case 1:
                rank=1 #High card
        #Create order list of hand type followed by individual card ranks
        card_rank='23456789TJQKA' #Individual card ranks from lowest to highest
        self.order=[]
        self.order.append(rank)
        self.order.append([card_rank.index(i) for i in self.s])
    
    def __str__(self) -> str:
        return(self.s)
    
    def __repr__(self) -> str:
        return(f'Hand({self.s})')

class Joker_Hand():
    def __init__(self,s) -> None:
        self.s=s
        counter=Counter(s) #Convert string into Counter object
        counter_non_J=counter.copy()
        counter_non_J.pop('J',None) #Copy of counter with no jokers
        #Resolve jokers
        J_num=counter['J'] #Number of jokers
        if 0<J_num<5:
            max_non_J=counter_non_J.most_common()[0][0] #Most common non-joker card
            del counter['J'] #Convert jokers into most popular non-joker card
            counter[max_non_J]+=J_num 

        #Work out what type of hand
        mx=max(counter.values())
        match mx:
            case 5:
                rank=7 #5 of a kind
            case 4:
                rank=6 #4 of a kind
            case 3:
                if 2 in counter.values():
                    rank=5 #Full House
                else:
                    rank=4 #3 of a kind
            case 2:
                if len([x for x in counter.values() if x==2])==2:
                    rank=3 #2 pair
                else:
                    rank=2 #1 pair
            case 1:
                rank=1 #High card
        #Create order list of hand type followed by individual card ranks
        card_rank_J='J23456789TQKA' #Individual card ranks from lowest to highest, with Joker as lowest
        self.order=[]
        self.order.append(rank)
        self.order.append([card_rank_J.index(i) for i in self.s])
    
    def __str__(self) -> str:
        return(self.s)
    
    def __repr__(self) -> str:
        return(f'JHand({self.s})')

def import_hands(part):
    hands=[] #List of hands (as Hand objects) and their bids
    for i in input:
        if part==1:
            hand=(Hand(i.split()[0]),int(i.split()[1]))
        elif part==2:
            hand=(Joker_Hand(i.split()[0]),int(i.split()[1]))
        hands.append(hand)

    hands_sorted=sorted(hands,key=lambda x:x[0].order)
    return(hands_sorted)

def total_winnings(hands):
    sum=0
    for i in range(len(hands)):
        sum+=(i+1)*hands[i][1]
    return(sum)

hands=import_hands(1)
print(total_winnings(hands))

hands=import_hands(2)
print(total_winnings(hands))