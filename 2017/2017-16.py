#Advent of Code 2017 Day 16

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-16.txt')
contents = f.read()
file_as_list = contents.splitlines()
instrs=file_as_list[0].split(',')

progs='abcdefghijklmnop'
#progs='abcde'
#instrs=['s1','x3/4','pe/b']

def solveA(instrs,progs): #Apply list of instructions to programs
    lnP=len(progs)
    for inst in instrs:
        if inst[0]=='s': #Spin instruction
            lnS=int(inst[1:])
            progs=progs[lnP-lnS:]+progs[:lnP-lnS]
        elif inst[0]=='x': #Exchange instruction
            posA=int(inst[1:].split('/')[0]) #First position to switch
            posB=int(inst[1:].split('/')[1]) #Second position to switch
            pos1=min(posA,posB)
            pos2=max(posA,posB)
            progs=progs[:pos1]+progs[pos2]+progs[pos1+1:pos2]+progs[pos1]+progs[pos2+1:]
        elif inst[0]=='p': #Partner instruction
            posA=progs.index(inst[1:].split('/')[0]) #Index of first partner
            posB=progs.index(inst[1:].split('/')[1]) #Index of second partner
            pos1=min(posA,posB)
            pos2=max(posA,posB)
            progs=progs[:pos1]+progs[pos2]+progs[pos1+1:pos2]+progs[pos1]+progs[pos2+1:]
    return(progs)
            
retA=solveA(instrs,progs)

def solveB(instrs,progs,reps): #Repeated dances
    progs0=progs[:]
    progs1=solveA(instrs,progs) #Position after one dance
    for r in range(reps):
        if r%10000000==0:
            print('Dance '+str(r+1))
        progs=solveA(instrs,progs)
        if progs==progs0:
            return(r+1)
    progout=''.join(progs)
    return(progout)

#retB=solveB(instrs,progs,1000000000)
cyc=solveB(instrs,progs,1000000) #number of dances for a full cycle
retB=solveB(instrs,progs,(1000000000%cyc))