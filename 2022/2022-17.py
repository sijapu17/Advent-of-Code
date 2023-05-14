#Advent of Code 2022 Day 17

from itertools import cycle

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-17.txt')
jets = f.read()
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-17shapes.txt')
contents = f.read()
shapetxt = contents.splitlines()

class Cave():
    def __init__(self,shapetxt,jets) -> None:
        self.jets=jets
        self.jet_id=-1
        self.shapes=[]
        self.shape_id=-1
        #Import shapes
        line=0
        shape=set()
        j=0
        while line<len(shapetxt):
            row=shapetxt[line]
            if len(row)==0:
                self.shapes.append(shape)
                shape=set()
                j=0
            elif len(row)>0:
                for i in range(len(row)):
                    if row[i]=='#':
                        shape.add(complex(i,j))
                j+=1
            line+=1
        self.shapes.append(shape) #Add final shape
        #Reflect shapes vertically
        self.heights=[]
        for s in self.shapes:
            self.heights.append(max([x.imag for x in s])-min([x.imag for x in s]))
        reflected=[] #Reflected shapes
        for n in range(len(self.shapes)):
            h=self.heights[n]
            s=self.shapes[n]
            reflected.append(set([complex(x.real,h-x.imag) for x in s]))
        self.shapes=reflected #Replace original shapes with reflected ones
        self.top=0 #Height of top rock (or floor)
        self.settled=set() #Set of currently settled rocks
        self.current=set() #Currently falling shape
    
    def next_shape(self): #Next shape in sequence
        self.shape_id=(self.shape_id+1)%len(self.shapes)
        return self.shapes[self.shape_id]

    def next_jet(self): #Next jet direction
        self.jet_id=(self.jet_id+1)%len(self.jets)
        return self.jets[self.jet_id]

    def drop_n_rocks(self,n): #Simulate dropping n rocks and return height
        for x in range(n):
            self.start_shape()
        return(self.top)
    
    def drop_n_rocks_cycle(self,n): #Calculate height after dropping n rocks by finding a cycle
        self.heights=[0]
        self.fingerprints={}
        c=0
        while c<n:
            c+=1
            self.start_shape()
            fingerprint=self.get_fingerprint()
            if fingerprint in self.fingerprints: #Check if fingerprint has already been seen
                c0=self.fingerprints[fingerprint]
                cycle=c-c0 #Length of cycle
                #n=a*cycle+(c0+b)
                a=(n-c0)//cycle
                b=(n-c0)%cycle
                #H[cycle]=H[c+b]-H[c0+b]
                i=c
                for i in range(b): #Drop more rocks to reach c+b
                    self.start_shape()
                h_cb=self.top
                h_c0b=self.heights[c0+b]
                h_cycle=h_cb-h_c0b
                #H[n]=a*H[cycle]+H[c0+b]
                h_n=a*h_cycle+h_c0b
                return(h_n)
 
            #If fingerprint is new, add to dictionaries
            self.fingerprints[fingerprint]=c
            self.heights.append(self.top)


    def start_shape(self): #Place new shape at start point
        shape=self.next_shape()
        vector=complex(3,self.top+4)
        self.current=set([x+vector for x in shape])
        #print('A new rock begins falling')
        #print(self)
        self.move_horizontal()

    def move_horizontal(self): #Move shape horizontally according to jet stream
        dir=self.next_jet()
        if dir=='<': #Left move
            vector=complex(-1,0)
            moveable=min([x.real for x in self.current])>1 #Check shape is not touching left wall
            txt='Jet of gas pushes rock left'
        elif dir=='>': #Right move
            vector=complex(1,0)
            moveable=max([x.real for x in self.current])<7 #Check shape is not touching right wall
            txt='Jet of gas pushes rock right'
        if moveable:
            new=set([x+vector for x in self.current])
            if new.isdisjoint(self.settled): #Check if shape would hit settled rocks if moved
                self.current=new
        else:
            txt+=', but nothing happens'
        #print(txt)
        #print(self)
        self.move_down()

    def move_down(self): #Move shape one step downwards, and check if it has landed
        new=set([x+complex(0,-1) for x in self.current])
        if new.isdisjoint(self.settled) and min([x.imag for x in new])>0: #Check if shape would hit settled rocks or floor if dropped
            self.current=new
            #print('Rock falls 1 unit')
            #print(self)
            self.move_horizontal()
        else:
            #Add new rocks to settled set
            for c in self.current:
                self.settled.add(c)
                if c.imag>self.top:
                    self.top=int(c.imag)
            #print('Rock falls 1 unit, causing it to come to rest')
            #print(self)

    def get_fingerprint(self): #Encode current state for cycle detection
        state=0
        e=1
        for j in range(5):
            for i in range(9):
                if complex(i,self.top-j) in self.settled:
                    state+=2**e
                    e+=1
        return ((state,self.shape_id,self.jet_id))


    def __str__(self) -> str:
        ret=''
        top=int(max(self.top,max([x.imag for x in self.current])))
        z=len(str(top)) #Zero-padding length
        for j in range(top,-1,-1):
            ret+=str(j).zfill(z)
            for i in range(9):
                if i==0 or i==8:
                    ret+='|'
                elif j==0:
                    ret+='-'
                elif complex(i,j) in self.settled:
                    ret+='#'
                elif complex(i,j) in self.current:
                    ret+='@'
                else:
                    ret+='.'
            ret+='\n'
        ret+=' '*z
        for i in range(9):
            ret+=str(i)
        return(ret+'\n')



cave=Cave(shapetxt,jets)
print(cave.drop_n_rocks(2022))
cave=Cave(shapetxt,jets)
print(cave.drop_n_rocks_cycle(1000000000000))