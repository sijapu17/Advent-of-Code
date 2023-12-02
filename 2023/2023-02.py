#Advent of Code 2023 Day 2

from functools import reduce
from math import prod

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-02.txt')
contents = f.read()
input = contents.splitlines()

#Group of red, green and blue cubes
class rgb():
    def __init__(self,vals:list =[0,0,0]) -> None:
        assert len(vals)==3, "vals should be length 3"
        self.vals=vals

    def __add__(self,other): #Add two rgb groups together
        return(rgb([sum(x) for x in zip(self.vals, other.vals)]))

    def __sub__(self,other): #Subtract one rgb group from another
        return(rgb([a-b for a,b in zip(self.vals, other.vals)]))
        
    def max(self,other): #Take itemwise max of two groups
        return(rgb([max(x) for x in zip(self.vals, other.vals)]))

    def contains(self,other): #Test whether a group fully contains another
        return(min((self-other).vals)>=0)
    
    def power(self): #Power value equals rgb values multiplied together
        return(prod(self.vals))
    
    def __repr__(self) -> str:
        return(f'rgb({self.vals})')
    
    def __str__(self) -> str:
        return(self.__repr__())

def read_games(input):
    games={}
    n=0
    for game in input: #Loop through games
        rounds=game.split(': ')[1].split('; ')
        round_list=[]
        for round in rounds: #Loop through rounds within a game           
            cubes=rgb() #Empty group of cubes
            cube_types=round.split(', ')
            for cube_type in cube_types: #Loop through cubes within a round
                words=cube_type.split()
                match words[1]:
                    case ('red'):
                        cubes+=rgb([int(words[0]),0,0])
                    case ('green'):
                        cubes+=rgb([0,int(words[0]),0])                        
                    case ('blue'):
                        cubes+=rgb([0,0,int(words[0])])
            round_list.append(cubes)
        n+=1
        games[n]=round_list
    return(games)

games=read_games(input)

def count_possible_games(games: dict,big_bag:rgb = rgb([12,13,14])):
    score=0
    for id, rounds in games.items():
        flag=1
        for round in rounds:
            if not big_bag.contains(round):
                flag=0
        score+=id*flag
    return(score)

def calculate_power(games: dict):
    score=0
    for rounds in games.values():
        max_bag:rgb=reduce(lambda x,y: x.max(y), rounds)
        score+=max_bag.power()
    return(score)

print(count_possible_games(games))
print(calculate_power(games))