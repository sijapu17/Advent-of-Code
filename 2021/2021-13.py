#Advent of Code 2021 Day 13
import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-13.txt')
contents = f.read()
inp = contents.splitlines()

class Paper():
    def __init__(self,inp) -> None:
        self.dots=set()
        self.folds=[]
        n=0
        while len(inp[n])>0: #Import dot positions
            i,j=(int(x) for x in inp[n].split(','))
            self.dots.add(complex(i,j))
            n+=1
        n+=1
        p=re.compile('^fold along (x|y)=(\d+)$')
        while n<len(inp): #Import fold instructions
            m=re.match(p,inp[n])
            self.folds.append((m.group(1),int(m.group(2))))
            n+=1

    def __str__(self) -> str:
        maxX=int(max([x.real for x in self.dots]))
        maxY=int(max([x.imag for x in self.dots]))
        ret=''
        for j in range(maxY+1):
            for i in range(maxX+1):
                if complex(i,j) in self.dots:
                    ret+='#'
                else:
                    ret+='.'
            ret+='\n'
        return(ret)

    def next_fold(self): #Perform next fold in the list
        (dir,loc)=self.folds.pop(0)
        if dir=='x':
            self.fold_horizontal(loc)
        elif dir=='y':
            self.fold_vertical(loc)

    def fold_all(self): #Perform every fold in turn
        while len(self.folds)>0:
            self.next_fold()
    
    def count_dots(self): #Count number of dots on paper
        return(len(self.dots))

    def fold_vertical(self,row): #Perform a vertical fold
        dots=set() #New dot positions
        for d in self.dots:
            if d.imag<row: #If dot is above fold, it stays in the same position
                dots.add(d)
            else: #If dot is below fold, it moves up to the mirrored position
                y=2*row-d.imag
                dots.add(complex(d.real,y))
        self.dots=dots #Overwrite old dot map with new one

    def fold_horizontal(self,col): #Perform a horizontal fold
        dots=set() #New dot positions
        for d in self.dots:
            if d.real<col: #If dot is above fold, it stays in the same position
                dots.add(d)
            else: #If dot is to the right of fold, it moves left to the mirrored position
                x=2*col-d.real
                dots.add(complex(x,d.imag))
        self.dots=dots #Overwrite old dot map with new one

paper=Paper(inp)
paper.next_fold()
print(paper.count_dots())
paper.fold_all()
print(paper)