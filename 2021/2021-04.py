f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-04.txt')
contents = f.read()
inp = contents.splitlines()

class Board(): #Single bingo Board
    def __init__(self,inp):
        self.dim=len(inp) #Dimension of square board
        self.numbers={} #Dict of numbers on the board, indexed by position
        self.complete=False #Flag for board completeness
        for y in range(self.dim):
            for x in range(self.dim):
                self.numbers[complex(x,y)]=int(inp[y].split()[x])
                
    def check_full_row(self,called,y): #Return True if all numbers in row have been called
        for x in range(self.dim):
            if self.numbers[complex(x,y)] not in called:
                return(False)
        return(True)
        
    def check_full_col(self,called,x): #Return True if all numbers in column have been called
        for y in range(self.dim):
            if self.numbers[complex(x,y)] not in called:
                return(False)
        return(True)
        
    def check_board(self,called): #Return True if any row or column is full
        for y in range(self.dim): #Check all rows
            if self.check_full_row(called,y):
                self.complete=True
                return(True)
        for x in range(self.dim): #Check all columns
            if self.check_full_col(called,x):
                self.complete=True
                return(True)
        return(False)
        
    def sum_uncalled(self,called): #Sum of uncalled numbers on board
        s=0
        for y in range(self.dim):
            for x in range(self.dim):
                if self.numbers[complex(x,y)] not in called:
                    s+=self.numbers[complex(x,y)]
        return(s)
                

class Bingo_System():
    def __init__(self,inp):
        self.to_call=[int(x) for x in inp[0].split(',')] #List of numbers to be called
        self.called=set()
        self.n_boards=0 #Number of boards in play
        i=2 #Read in boards one at a NotImplemented
        self.boards=set() #Collection of all boards, in no particular order
        while i<len(inp):
            self.boards.add(Board(inp[i:i+5]))
            self.n_boards+=1
            i+=6
            
    def call_next(self): #Call next number, stopping if a board is complete
        num=self.to_call.pop(0)
        self.called.add(num)
        for b in self.boards:
            if not b.complete: #Skip board if it is already complete
                if b.check_board(self.called):
                    score=num*b.sum_uncalled(self.called)
                    return(score)
                
    def winning_score(self):
        while True:
            score=self.call_next()
            if type(score) is int:
                return(score)

    def call_next_pt2(self): #Call next number but do not stop once a board is complete
        num=self.to_call.pop(0)
        print('{} called'.format(num))
        self.called.add(num)
        for b in self.boards:
            if not b.complete: #Skip board if it is already complete
                if b.check_board(self.called):
                    score=num*b.sum_uncalled(self.called)
                    print(score)
                    
    def all_scores(self):
        while len(self.to_call)>0:
            score=self.call_next_pt2()

system=Bingo_System(inp)
print(system.winning_score())
system=Bingo_System(inp)
system.all_scores()