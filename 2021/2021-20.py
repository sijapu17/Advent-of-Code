#Advent of Code 2021 Day 20
from collections import defaultdict
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-20.txt')
contents = f.read()
inp = contents.splitlines()

class Image():
    def __init__(self,inp,max_steps) -> None:
        self.steps=0
        self.max_steps=max_steps
        self.algorithm=inp[0]
        self.dimX=len(inp[2])
        self.dimY=len(inp[2:])
        self.map=defaultdict(self.border)
        for j in range(self.dimY):
            for i in range(self.dimX):
                self.map[complex(i,j)]=inp[j+2][i]

    def __str__(self) -> str:
        ret=''
        for j in range(-2*self.max_steps,self.dimY+2*self.max_steps+1):
            for i in range(-2*self.max_steps,self.dimX+2*self.max_steps+1):
                ret+=self.map[complex(i,j)]
            ret+='\n'
        return(ret)

    def run_step(self): #Run 1 step of image enhancement
        new_map=defaultdict(self.border)
        for j in range(-2*self.max_steps,self.dimY+2*self.max_steps+1): #Border may encroach into original image up to one row/column per step
            for i in range(-2*self.max_steps,self.dimX+2*self.max_steps+1):
                a=self.alg_num(complex(i,j))
                new_map[complex(i,j)]=self.algorithm[a]
        self.map=new_map
        self.steps+=1
        #print(self)

    def run_all_steps(self): #Run all steps
        while self.steps<self.max_steps:
            self.run_step()

    def count_lights(self):
        return(len([x for x in self.map.values() if x=='#']))

    def border(self): #Determine status of infinite border, based on current step
        if self.algorithm[0]=='.':
            return('.')
        elif self.algorithm[0]=='#':
            if self.steps%2==0:
                return('.')
            else:
                return('#')

    def alg_num(self,pos): #Determine algorithm number to use for position, based on 3*3 grid surrounding its position
        x=0
        mul=256
        for j in (-1,0,1):
            for i in (-1,0,1):
                if self.map[pos+complex(i,j)]=='#':
                    x+=mul
                mul/=2
        return(int(x))

image=Image(inp,2)
image.run_all_steps()
print(image.count_lights())
image=Image(inp,50)
image.run_all_steps()
print(image.count_lights())