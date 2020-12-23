#Advent of Code 2020 Day 23

input='364289715'
#input='389125467'

def parse(input,part=2): #Parse input into linked list deck
    inp=[int(x) for x in input]
    deck=Linked_List(inp)
    if part==2: #Extend deck to size 1,000,000
        deck.insert(range(10,1000001),inp[-1])
    deck.update_max()
    return(deck)

class Linked_List(): #Linked List
    
    def __init__(self,input):
        self.d={} #Dict mapping each cup to the cup after it
        self.current=input[0] #Starting element
        for i in range(len(input)-1):
            self.d[input[i]]=input[i+1]
        self.d[input[-1]]=input[0] #Map last cup to first to complete the circle

    def next(self): #Update current to next element
        self.current=self.d[self.current]

    def update_max(self): #Update max value in dict
        self.mx=max(self.d)

    def insert(self,to_add,after): #Insert 'to_add' following 'after'
        dest=self.d[after]
        if type(to_add)=='int': #Insert single int
            self.d[after]=to_add #Map from 'after' to 'to_add'
            self.d[to_add]=dest #Map 'to_add' to 'dest'
        else: #Insert list of ints
            self.d[after]=to_add[0] #Map from 'after' to 'to_add'
            for i in range(len(to_add)-1): #Map each element of 'to_add' to the next one
                self.d[to_add[i]]=to_add[i+1]
            self.d[to_add[-1]]=dest #Map end of 'to_add' to 'dest'

    def remove(self,after,n=3): #Remove n elements following 'after'
        out=self.d[after] #out is (first) element to remove        
        if n==1:
            self.d[after]=self.d[out] #Modify after so it skips out
            del self.d[out] #Remove out from dict
            return(out)
        else:
            out_list=[] #List of removed elements
            for i in range(n):
                out_list.append(out)
                next=self.d[out] #Next element to remove
                del self.d[out] #Remove out from dict
                out=next
            self.d[after]=next #Link element before removed block to next element after
            return(out_list)



def run_step(deck): #Run one step of the process on the deck
    to_move=deck.remove(deck.current,n=3) #Remove 3 cups after current
    dest_val=deck.current-1 #Find first cup lower than current
    while dest_val not in deck.d:
        dest_val-=1
        if dest_val<1: #Wrap round to highest card if necessary
            dest_val=deck.mx
    deck.insert(to_move,dest_val)
    deck.next() #Update current

def run_n_steps(deck,n,part):            
    #print(deck)
    for i in range(n):
        if i%100000==1:
            print('Step '+str(i))
        run_step(deck)
        #print(deck)
    if part==1:
        #Print all cups in order after 1 (except 1 itself)
        ret=''
        x=deck.d[1]
        while x != 1:
            ret+=str(x)
            x=deck.d[x]
        return(ret)

    elif part==2:
        #Find product of 2 cups directly after 1
        x=deck.d[1]
        print(x)
        y=deck.d[x]
        print(y)
        return(x*y)



deck=parse(input,part=1)
print(run_n_steps(deck,100,part=1))

deck=parse(input,part=2)
print(run_n_steps(deck,10000000,part=2))