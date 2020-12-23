from collections import deque

input='364289715'
#input='389125467'

def parse(input): #Parse input into deque
    deck=deque()
    for i in input:
        deck.append(int(i))
    return(deck)



def run_n_steps(deck,n):
    #print(deck)
    for i in range(n):
        run_step(deck)
        #print(deck)
    #Rotate around so 1 is at end
    one_pos=deck.index(1)
    deck.rotate(-1*(one_pos+1))
    print(deck)
    ret='' #Create string of every card except 1
    while len(deck)>1:
        ret+=str(deck.popleft())
    return(ret)


def run_step(deck): #Run one step of the process on the deck
    current=deck[0]
    deck.rotate(-1) #Rotate so current is moved to end
    to_move=[]
    for i in range(3): #Take next 3 cups out of deck
        to_move.append(deck.popleft())
    dest_val=current-1 #Find first cup lower than current
    while dest_val not in deck:
        dest_val-=1
        if dest_val<1: #Wrap round to highest card if necessary
            dest_val=9
    dest_pos=deck.index(dest_val)+1
    for i in range(3):
        deck.insert(dest_pos,to_move.pop())


#deck=parse(input)
#print(run_n_steps(deck,100))