#Advent of Code 2022 Day 8

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-08.txt')
contents = f.read()
inp = contents.splitlines()

class Forest():
    def __init__(self,inp) -> None:
        self.dimX=len(inp[0])
        self.dimY=len(inp)
        self.trees={}
        for j in range(self.dimY):
            for i in range(self.dimX):
                self.trees[complex(i,j)]=int(inp[j][i])

    def __str__(self) -> str:
        ret=''
        for j in range(self.dimY):
            for i in range(self.dimX):
                ret+=str(self.trees[complex(i,j)])
            ret+='\n'
        return(ret)


    def map_visible(self) -> str: #Draw map where 1=visible, 0=not visible
        ret=''
        for j in range(self.dimY):
            for i in range(self.dimX):
                ret+=str(int(self.is_visible(complex(i,j))))
            ret+='\n'
        return(ret)

    def is_visible(self,c:complex): #Return bool of whether tree at position c is visible
        x=int(c.real)
        y=int(c.imag)
        #Tallest tree in each direction, in order [w,e,n,s]
        max_in_dirs=[max([self.trees[complex(i,y)] for i in range(x)]+[-1]),
                     max([self.trees[complex(i,y)] for i in range(x+1,self.dimX)]+[-1]),
                     max([self.trees[complex(x,j)] for j in range(y)]+[-1]),
                     max([self.trees[complex(x,j)] for j in range(y+1,self.dimY)]+[-1])]
        #Tree is visible iff it is taller than all trees in at least one direction
        return(self.trees[c]>min(max_in_dirs))
    
    def count_visible(self): #Count number of visible trees in forest
        return(sum([self.is_visible(x) for x in self.trees]))

    def scenic_score(self,c:complex): #Return scenic score of given position
        score=1
        dirs=(complex(1,0),complex(-1,0),complex(0,1),complex(0,-1))
        height=self.trees[c]
        for d in dirs:
            pos=c
            n=0
            while True:
                pos+=d
                if pos not in self.trees:
                    break
                n+=1                
                if self.trees[pos]>=height or pos+d not in self.trees:
                    break
            score*=n
        return(score)
    
    def best_score(self): #Return highest scenic score possible for any tree
        return(max([self.scenic_score(c) for c in self.trees]))
        
forest =Forest(inp)
print(forest)
print(forest.count_visible())
print(forest.best_score())