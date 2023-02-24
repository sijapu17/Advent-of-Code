#Advent of Code 2022 Day 11

from collections import deque

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-11.txt')
contents = f.read()
inp = contents.splitlines()

class System:
    def __init__(self,inp,part) -> None:
        self.part=part #Part 1 or 2
        p=0 #Line pointer
        self.monkeys={}
        self.lcm=1 #Calculate common multiple
        while p<len(inp):
            id=int(inp[p][7])
            p+=1
            items=deque([int(x) for x in inp[p].split(': ')[1].split(', ')])
            p+=1
            op=inp[p].split(' = ')[1]
            p+=1
            test_div=int(inp[p].split()[-1])
            self.lcm*=test_div #Increase common multiple
            p+=1
            dest_true=int(inp[p].split()[-1])
            p+=1
            dest_false=int(inp[p].split()[-1])
            self.monkeys[id]=Monkey(self,id,items,op,test_div,dest_true,dest_false)
            p+=2

    def run_n_rounds(self,n): #Run n rounds of keep away
        for i in range(n):
            self.run_round()
        #Inspection totals
        totals=sorted([x.inspections for x in self.monkeys.values()])
        return(totals[-1]*totals[-2])

    def run_round(self): #Run 1 round of keep away
        for n in range(len(self.monkeys)):
            current=self.monkeys[n]
            while len(current.items)>0:
                current.process_item(current.items.popleft())

class Monkey():
    def __init__(self,system,id,items,op,test_div,dest_true,dest_false) -> None:
        self.id=id
        self.items=items
        self.op=op
        self.test_div=test_div
        self.dest_true=dest_true
        self.dest_false=dest_false
        self.inspections=0

    def __str__(self) -> str:
        return(f'Monkey {self.id}: {self.items}')
    
    def __repr__(self) -> str:
        return(self.__str__())

    def receive_item(self,item): #Receive item from another monkey, put to back of queue
        self.items.append(item)

    def process_item(self,item): #Inspect, boredom, test, send
        item=self.inspect(item)
        if system.part==1:
            item//=3
        item%=system.lcm #Reduce to modulo of LCM to keep numbers from getting too big
        if item%self.test_div==0:
            system.monkeys[self.dest_true].receive_item(item)
        else:
            system.monkeys[self.dest_false].receive_item(item)

    def inspect(self,item): #Inspect item by performing operation on it, returning new worry level
        self.inspections+=1
        match self.op.split():
            case ['old','*','old']:
                return(item*item)
            case ['old','*',num]:
                return(item*int(num))
            case ['old','+',num]:
                return(item+int(num))
                
system=System(inp,1)
print(system.run_n_rounds(20))
system=System(inp,2)
print(system.run_n_rounds(10000))