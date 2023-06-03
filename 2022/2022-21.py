#Advent of Code 2022 Day 21

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-21.txt')
contents = f.read()
input = contents.splitlines()

class System():
    def __init__(self,input) -> None:
        self.monkeys={}
        for e in input:
            equation=e.split(': ')
            self.monkeys[equation[0]]=equation[1].split()

    def evaluate_monkey(self,name): #Recursively evaluate named monkey
        equation=self.monkeys[name]
        if len(equation)==1:
            return(int(equation[0]))
        else:
            match equation[1]:
                case '+':
                    return(self.evaluate_monkey(equation[0])+self.evaluate_monkey(equation[2]))
                case '-':
                    return(self.evaluate_monkey(equation[0])-self.evaluate_monkey(equation[2]))
                case '*':
                    return(self.evaluate_monkey(equation[0])*self.evaluate_monkey(equation[2]))
                case '/':
                    return(self.evaluate_monkey(equation[0])/self.evaluate_monkey(equation[2]))
                
    def find_correct_humn(self): #Find correct value of humn so both sides of root are equal
        self.monkeys['root']=[self.monkeys['root'][0],'-',self.monkeys['root'][2]] #Change root to subtract so we can check for equality
        self.monkeys['humn']=[0] #Starting point for humn, yields positive root
        upper=10
        #Find intial bounds for binary search
        while True:
            self.monkeys['humn']=[upper]
            res=self.evaluate_monkey('root')
            print(f'{upper}: {res}')
            if self.evaluate_monkey('root')<0:
                break
            lower=upper
            upper*=10
        #Narrow down to solution
        while True:
            mid=int((lower+upper)/2)
            self.monkeys['humn']=[mid]
            res=self.evaluate_monkey('root')
            print(f'{mid}: {res}')
            if res==0:
                print(f'Solution found: {mid}')
                break
            elif res>0: #Case where mid is too low
                lower=mid
            elif res<0: #Case where mid is too high
                upper=mid
                
system=System(input)
print(int(system.evaluate_monkey('root')))
system.find_correct_humn()