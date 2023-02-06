#Advent of Code 2022 Day 7

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-07.txt')
contents = f.read()
input = contents.splitlines()

class Folder():
    def __init__(self,name,parent) -> None:
        self.name=name
        self.size=0
        self.parent=parent #Parent folder

    def add_file(self,size):
        self.size+=size
        if self.name!='/': #Update size of all parent folders
            self.parent.add_file(size)

    def __str__(self) -> str:
        return(f'F{self.name}-{self.size}')

    def __repr__(self) -> str:
        return(f'F{self.name}-{self.size}')


def parse(input): #Create folder structure
    loc=[] #Location
    folders={}
    folders[str(loc)]=Folder('/',None)
    p_c=re.compile('^\$ cd (.+)$') #regex for commands
    p_f=re.compile('^(\d+) .+$') #regex for file
    p_d=re.compile('^dir (\w+)$') #regex for directory
    for x in input:
        if x=='$ cd /':
            loc=[]  
        elif x=='$ cd ..':
            loc=loc[:-1] #Remove final folder to move up one level
        elif re.search(p_c,x): #Command to move into specified folder
            m=p_c.match(x)
            parent=folders[str(loc)]
            loc.append(m.group(1))
            if str(loc) not in folders:
                folders[str(loc)]=Folder(str(loc),parent)
        elif re.search(p_f,x): #File
            m=p_f.match(x)
            folders[str(loc)].add_file(int(m.group(1)))
    return(folders)

def count_le_n(folders,n): #Sum size of folders with at most size n
    total=0
    for f in folders.values():
        if f.size<=n:
            total+=f.size
    return(total)

def find_smallest_delete(folders,total,req): #Find smallest folder that can be deleted to reach the required free space
    available=total-folders['[]'].size
    size_to_delete=req-available
    smallest=float('Inf')
    for f in folders.values():
        if f.size>=size_to_delete and f.size<=smallest:
            smallest=f.size
    return(smallest)   

system=parse(input)
#print(count_le_n(system,100000))
print(find_smallest_delete(system,70000000,30000000))