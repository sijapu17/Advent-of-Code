#Advent of Code 2024 Day 22

from collections import defaultdict

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-22.txt')
contents = f.read()
input = [int(x) for x in contents.splitlines()]

def next_secret(s): #Calculate next secret number in sequence
    s_1=((s*64)^s)%16777216
    s_2=((s_1//32)^s_1)%16777216
    s_3=((s_2*2048)^s_2)%16777216
    return(s_3)

def secret_n(s,n): #Calculate n secret numbers from s
    for _ in range(n):
        s=next_secret(s)
    return(s)

def price_n(s,n): #Calculate n price changes from s
    prices=[]
    changes=[]
    for _ in range(n):
        next_s=next_secret(s)
        prices.append(next_s%10)
        changes.append(next_s%10-s%10)
        s=next_s
    return((tuple(prices),tuple(changes)))

print(sum([secret_n(s,2000) for s in input])) #Part 1

#Calculate price history for every banana
class Banana():

    def __init__(self,secret):
        self.secret=secret
        self.price_0=secret%10
        self.prices, self.changes=price_n(secret,2000)

    def __str__(self):
        return(f'Banana {self.secret}')

    def __repr__(self):
        return(f'Banana {self.secret}')
    
    def price_t(self,t): #Calculate price at time t
        return(self.prices[t])
        
    def seq_t(self,t): #Return sequence at time t
        return(self.changes[t:t+4])
    
bananas=[Banana(s) for s in input]

sequence_prices=defaultdict(int)
for b in bananas:
    sequences_found=set()
    for t in range(len(b.changes)-4):
        seq=b.seq_t(t)
        if seq not in sequences_found:
            sequences_found.add(seq)
            sequence_prices[seq]+=b.price_t(t+3)

print(max(sequence_prices.values()))