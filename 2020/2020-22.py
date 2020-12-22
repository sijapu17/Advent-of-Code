#Advent of Code 2020 Day 22

from collections import deque

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-22.txt')
state = f.read()
input=state.splitlines()



class Game():
    def __init__(self,input):
        self.cards={}
        self.cards['p1']=deque()
        self.cards['p2']=deque()
        i=1    
        while len(input[i])>0:
            self.cards['p1'].append(int(input[i]))
            i+=1
        i+=2
        while i<len(input):
            self.cards['p2'].append(int(input[i]))
            i+=1    

    def play_round(self,deck1,deck2,level,round,recursive=True):
        #print('\nLevel '+str(level)+' Round '+str(round))
        #print('Player 1: '+str(deck1))
        #print('Player 2: '+str(deck2))
        #Compare two top cards
        cards=[deck1.popleft(),deck2.popleft()]
        #Find winner
        if recursive and len(deck1)>=cards[0] and len(deck2)>=cards[1]:
            subdeck1=deque(list(deck1)[:cards[0]])
            subdeck2=deque(list(deck2)[:cards[1]])
            winner=self.play_game(subdeck1,subdeck2,recursive=True,level=level+1)
        else:
            if cards[0]>cards[1]:
                winner='p1'
            else:
                winner='p2'
        #Append the two cards to the bottom of the winner's deck, highest first
        if winner=='p1':
            deck1.append(cards[0])
            deck1.append(cards[1])
        else:
            deck2.append(cards[1])
            deck2.append(cards[0])

    def play_game(self,deck1,deck2,recursive=True,level=1):
        decks={'p1':deck1,'p2':deck2} #Map players to decks
        round=0
        prev_states=set() #Set of previously seen states
        state=(hash(tuple(deck1)),hash(tuple(deck2)))

        while min(len(deck1),len(deck2))>0 and state not in prev_states:
            prev_states.add(state)
            round+=1
            self.play_round(deck1,deck2,level=level,round=round,recursive=recursive)
            state=(hash(tuple(deck1)),hash(tuple(deck2)))
        if len(deck1)>0 or state in prev_states:
            winner='p1'
        else:
            winner='p2'

        if level==1: #Only print score for top-level game
            score=self.score_hand(decks[winner])
            print(score)
        
        return(winner)

    def score_hand(self,hand): #For each card from bottom to top, score 1...n * value of card
        score=0
        dim=len(hand)
        for i in range(len(hand)):
            score+=(dim-i)*hand[i]
        return(score)


game=Game(input)
print(game.play_game(game.cards['p1'],game.cards['p2'],recursive=False))
print(game.play_game(game.cards['p1'],game.cards['p2'],recursive=True)) #8771 too low