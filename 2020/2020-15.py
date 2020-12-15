#Advent of Code 2020 Day 15

input=[19,20,14,0,9,1]
#input=[0,3,6]

class Game():

    def __init__(self,input):
        self.last_seen={}
        for i in range(len(input)-1): #Don't add in last starting number yet
            self.last_seen[input[i]]=i+1
        self.next=input[-1] #Start game with last starting number
        self.turn=len(input)-1

    def take_turn(self): #Take 1 turn
        self.turn+=1
        self.current=self.next
        if self.current in self.last_seen: #If number has been seen, next number is gap in turns since last seen
            self.next=self.turn-self.last_seen[self.current]
        else:
            self.next=0
        self.last_seen[self.current]=self.turn

    def take_n_turns(self,n) : #Take n turns
        while self.turn<n:
            self.take_turn()
            if self.turn%300000==1:
                print('Turn {0}: {1}'.format(self.turn,self.current))
        return(self.current)

    

game=Game(input)
print(game.take_n_turns(2020))
print(game.take_n_turns(30000000))