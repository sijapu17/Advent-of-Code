#Advent of Code 2020 Day 8

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-08.txt')
contents = f.read()
input=contents.splitlines()

class Console(): #Games console

    def __init__(self,input):
        self.code=dict() #Convert code to dict to allow pointer to reach new memory
        self.size=len(input)
        for i in range(self.size):
            self.code[i]=dict()
            self.code[i]['op']=input[i].split()[0]
            self.code[i]['val']=int(input[i].split()[1])
        self.point=0 #Position of code pointer
        self.acc=0 #Global accumulator register
        self.terminated=False #Initialise termination detection

    def switch_line(self,n): #Switches line n from jmp to nop or vice versa
        if self.code[n]['op']=='jmp':
            self.code[n]['op']='nop'
        elif self.code[n]['op']=='nop':
            self.code[n]['op']='jmp'

    def step(self): #Runs current step of program

        if self.point>=self.size: #If pointer passes the end of the code, terminate
            self.terminated=True       
        else:
            line=self.code[self.point] #Find current line of code

            if line['op']=='acc': #Adjust accumulator
                self.acc+=line['val']
                self.point+=1
            elif line['op']=='jmp': #Move pointer by specified amount
                self.point+=line['val']
            elif line['op']=='nop': #No operation, continue to next instruction
                self.point+=1

    def run_until_repeat(self): #Run until a line is reached for a second time

        visited=set()
        while self.point not in visited and not self.terminated:
            visited.add(self.point)
            self.step()
        return(self.acc)

console=Console(input)
print(console.run_until_repeat())

def find_switch(input): #Find one jmp/nop instruction to switch to make 
    j=0 #Loop through values of i until terminating switch is found
    while j<=len(input):
        console=Console(input)
        if console.code[j]['op'] != 'acc':
            console.switch_line(j)
            ret=console.run_until_repeat()
            if console.terminated:
                return(ret)
        j+=1

print(find_switch(input))
