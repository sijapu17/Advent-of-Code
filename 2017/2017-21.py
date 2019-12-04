#Advent of Code 2017 Day 21

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2017-21.txt')
contents = f.read()
input = contents.splitlines()
start=['.#.','..#','###']
#start=['..#.','####','#..#','.###']

in0=input[2].split(' => ')[0]
in0l=in0.split('/')
in0ll=[list(x) for x in in0l]

def transp(input): #Transpose input
    dim=len(input)
    out=['' for n in range(dim)]
    for i in range(dim):
        for j in range(dim):
            out[i]+=input[j][i]
    return(out)
            
def rotate(input): #Rotate input
    dim=len(input)
    out=['' for n in range(dim)]
    for i in range(dim):
        for j in range(dim):
            out[i]+=input[dim-1-j][i]
        #(i,j) -> (dim-j,i)
    return(out)

def createRecipes(input): #Create recipe dictionary, including rotations and tranposes
    recipes={}
    for l in input:
        pre=l.split(' => ')[0].split('/')
        post=l.split(' => ')[1].split('/')
        for n in range(4): #Rotate 4 times, transpose and rotate 4 more times to capture all versions
            pre=rotate(pre)
            recipes[tuple(pre)]=post
        pre=transp(pre)
        for n in range(4):
            pre=rotate(pre)
            recipes[tuple(pre)]=post
    return(recipes)

rec=createRecipes(input)

class Image():
    
    def __init__(self,start,recipes):
        self.grid=start
        self.recipes=recipes
        
    def splitChunks(self): #Split grid into 2x2 or 3x3 chunks
        dim=len(self.grid)
        if dim%2==0:
            cDim=2 #Break into 2x2 chunks
        elif dim%3==0:
            cDim=3 #Break into 3x3 chunks
        nChkRt=int(dim/cDim) #Number of chunks along one dimension
        chunks=[]
        for i in range(nChkRt):
            for j in range(nChkRt):
                chunk=[]
                for n in range(cDim):
                    chunk.append(self.grid[i*cDim+n][j*cDim:j*cDim+cDim])
                chunks.append(tuple(chunk))
        return(chunks)
    
    def enhance(self,chunks): #Update chunks based on enhancement rules
        out=[]
        for c in chunks:
            out.append(self.recipes[c])
        return(out)
    
    def rejoin(self,eChunks): #Rejoin enhanced chunks back into one grid
        chunksInRow=int(len(eChunks)**0.5)
        cLen=len(eChunks[0])
        dim=chunksInRow*cLen #Dimension of final grid
        #print(dim)
        #print(chunksInRow)
        out=['']*dim
        i=0
        d=0
        for ec in eChunks:
            #print(str(ec))
            for r in ec:
                #print('d='+str(d)+', i='+str(i))
                out[i]+=r
                i+=1
            d+=1
            if d<chunksInRow: #Join dim chunks before row is complete
                i-=cLen
            else:
                d=0
        return(out)
            
        
def solveA(input,nreps):
    
    image=Image(start,rec)
    for n in range(nreps):
        print(n)
        chunks=image.splitChunks()
        enh=image.enhance(chunks)
        rej=image.rejoin(enh)
        image.grid=rej
    sum=0
    for row in image.grid:
        sum+=row.count('#')
    return(sum)
        
    return(image.grid)
        
retA=solveA(input,18)
            
        
    