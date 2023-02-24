#Advent of Code 2022 Day 10

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-10.txt')
contents = f.read()
inp = contents.splitlines()

class Computer():

    def __init__(self,inp) -> None:
        self.x=1 #Register X
        self.cycle=0
        self.inp=inp
        self.display='' #String of #/. which will form display

    def next_cycle(self):
        self.cycle+=1
        #Signal strength (part 1)
        if self.cycle%40==20:
            #print(f'Cycle {self.cycle}: X={self.x}')
            self.strength+=(self.cycle*self.x)
        #Display (part 2)
        #print(f'Cycle {self.cycle}: X={self.x}')
        h_pos=((self.cycle-1)%40) #Horizontal position being drawn
        if abs(h_pos-self.x)<=1:
            self.display+='#'
        else:
            self.display+='.'
        #if self.cycle<25:
        #    print(self.display)
        if h_pos==39:
            self.display+='\n'

    def run_instructions(self):
        self.strength=0
        for line in inp:
            self.next_cycle()
            if line.split()[0]=='addx':
                self.next_cycle()
                self.x+=int(line.split()[1])
        print(self.display)
        return(self.strength)

computer=Computer(inp)
print(computer.run_instructions())