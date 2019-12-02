#Advent of Code 2015 Day 19

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2015-19.txt')
contents = f.read()
input = contents.splitlines()

def imp(input):
    rplcs=[] #List of possible replacements
    for each in input: #Find all possible replacements and starting molecule
        if len(each)>0 and each.find(' => ')>0:
            rplcs.append(tuple(each.split(' => ')))
        elif len(each)>0:
            mol=each
    return([rplcs,mol])

inB=imp(input)
#inA=[[('H','AA')],'HOH']

def solveA(inA):
    rplcs=inA[0]
    mol=inA[1]
    mols=set() #All possible molecules after one replacement
    mLen=len(mol)
    for rp in rplcs:
        inLn=len(rp[0])
        for i in range(mLen+1-inLn):
            if mol[i:i+inLn]==rp[0]:
                mols.add(mol[:i]+rp[1]+mol[i+inLn:])
    return(len(mols))
    

#retA=solveA(inA)

class Molecule():
    
    def __init__(self,name,subs):
        self.name=name
        self.subs=subs #Note: subs are from the end product
        self.Len=len(name)
        
def getShortest(mDict): #Return shortest molecule from list
    minName=None
    minLen=float('inf')
    for m in mDict.values():
        if m.Len<minLen:
            minName=m.name
            minLen=m.Len
    return(minName)
            

def solveB(inB):
    rplcs=inB[0]
    mols={}
    mols[inB[1]]=Molecule(inB[1],0)
    while len(mols)>0:
        mol=mols[getShortest(mols)] #Find shortest molecule
        name=mol.name
        if name=='e':
            return(mol)
        replaced=False
        for rp in rplcs: #Try to replace (backwards) from the end of the molecule
            outLn=len(rp[1])
            for i in reversed(range(mol.Len+1-outLn)):
                if name[i:i+outLn]==rp[1]:
                    name1=name[:i]+rp[0]+name[i+outLn:]
                    replaced=True
                    print(name+' -> '+name1)
                    if name1 in mols: #If molecule has been reached before then record minimum subs to reach
                        mols[name1].subs=min(mols[name1].subs,mols[name].subs+1)
                    else: #If molecule is new then add to dict
                        mols[name1]=Molecule(name1,mols[name].subs+1)     
                    break
        if replaced==False:
            del mols[name]
                
#retB=solveB(inB)
mol=inB[1]