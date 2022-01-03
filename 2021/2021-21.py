#Advent of Code 2021 Day 21
from functools import cache
from collections import defaultdict

#Player 1 starting position: 4
#Player 2 starting position: 9

def deterministic_die():
    result=0
    while True:
        if result==100:
            result=0
        result+=1
        #print(result)
        yield(result)

class Player():
    def __init__(self,start,name) -> None:
        self.name=name
        self.pos=start
        self.score=0

    def move(self,roll): #Move pawn forward
        self.pos+=roll
        while self.pos>10:
            self.pos-=10
        self.score+=self.pos

    def __str__(self) -> str:
        return(f'{self.name}: Space {self.pos}, score {self.score}')

def play_game(pos1,pos2):
    p1=Player(pos1,'Player 1')
    p2=Player(pos2,'Player 2')
    n_rolls=0
    die=deterministic_die()
    while True:
        #Player 1 turn
        roll=0
        for n in range(3): #Generate next 3 die rolls
            roll+=die.__next__()
        p1.move(roll)
        n_rolls+=3
        print(p1)
        if p1.score>=1000:
            ret=p2.score*n_rolls
            print(f'Player 1 wins after {n_rolls} rolls with {p1.score} vs {p2.score}. Return value {ret}')
            return()
        #Player 2 turn
        roll=0
        for n in range(3): #Generate next 3 die rolls
            roll+=die.__next__()
        p2.move(roll)
        n_rolls+=3
        print(p2)
        if p2.score>=1000:
            ret=p1.score*n_rolls            
            print(f'Player 2 wins after {n_rolls} rolls with {p2.score} vs {p1.score}. Return value {ret}')  
            return()  

play_game(4,9)

class Wins(): #Simple class for counting wins for p1 vs p2
    def __init__(self,p1,p2) -> None:
        self.p1=p1
        self.p2=p2

    def __add__(self,other): #Add 2 Wins objects together
        return(Wins(self.p1+other.p1,self.p2+other.p2))

    def max_score(self): #Return max score
        return(max(self.p1,self.p2))

    def __repr__(self) -> str:
        return(f'[{self.p1}, {self.p2}]')

    def __str__(self) -> str:
        return(self.__repr__())

@cache
def count_wins(pos1,pos2,score1,score2,turn='p1'): #Recursively count number of universes where each player wins
    global dist #Bring in pre-calculated distribution
    if score1>=21:
        return(Wins(1,0))
    elif score2>=21:
        return(Wins(0,1))
    else:
        wins=Wins(0,0)
        if turn=='p1': #Player 1 turns
            for a in range(1,4):
                for b in range(1,4):
                    for c in range(1,4):
                        new=((pos1-1+a+b+c)%10)+1 #New position after roll
                        wins+=count_wins(new,pos2,score1+new,score2,turn='p2')
        elif turn=='p2': #Player 2 turns
            for a in range(1,4):
                for b in range(1,4):
                    for c in range(1,4):
                        new=((pos2-1+a+b+c)%10)+1 #New position after roll
                        wins+=count_wins(pos1,new,score1,score2+new,turn='p1')
        return(wins)

scores=count_wins(4,9,0,0,turn='p1')
print(scores)
print(scores.max_score())