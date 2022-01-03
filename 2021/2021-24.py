#Advent of Code 2021 Day 24

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-24.txt')
contents = f.read()
inp = contents.splitlines()

#From manually decompiling code, following conditions must be met:
#i2+8=i3+11
#i6+2=i7+7
#i8+4=i9+6
#i5+12=i10+10
#i4+7=i11+15
#i1+12=i12+9
#i0+6=i13
#Simplified:
#i2=i3+3
#i6=i7+5
#i8=i9+2
#i5+2=i10
#i4=i11+8
#i1+3=i12
#i0+6=i13

#36969794979199 (Highest possible)
#11419161313147 (Lowest possible)

class Computer():
    def __init__(self,inp) -> None:
        self.code=inp[:]

    def valid_model(self,model): #Run whole program with given model number, returns validity as True/False 
        self.vars={'w':0,'x':0,'y':0,'z':0}
        self.model=[int(x) for x in str(model)]
        for line in self.code:
            self.run_line(line)
        return(self.vars['z']==0)

    def run_line(self,line): #Run single line of code
        l=line.split()
        type=l[0]
        if type=='inp':
            self.vars[l[1]]=self.model.pop(0)
        else: #Determine whether b is a variable or a constant
            if l[2] in 'wxyz':
                b=self.vars[l[2]]
            else:
                b=int(l[2])
            if type=='add':
                self.vars[l[1]]+=b
            if type=='mul':
                self.vars[l[1]]*=b            
            if type=='div':
                self.vars[l[1]]=int(self.vars[l[1]]//b)
            if type=='mod':
                self.vars[l[1]]%=b
            if type=='eql':
                if self.vars[l[1]]==b:
                    self.vars[l[1]]=1
                else:
                    self.vars[l[1]]=0
        
computer=Computer(inp)
print(computer.valid_model(36969794979199))
print(computer.valid_model(11419161313147))