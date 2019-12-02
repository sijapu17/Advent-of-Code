#Advent of Code 2015 Day 7

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-7b.txt')
contents = f.read()
input = contents.splitlines()

def AND(a,b):
    return(a & b)
def COPY(a):
    return(a)
def LSHIFT(a,b):
    return(a<<b)
def RSHIFT(a,b):
    return(a>>b)
def NOT(a):
    return(~a)
def OR(a,b):
    return(a|b)


def solveA(input):
    wires={} #Dictionary of wires
    instQ=[] #list of instructions left to implement
    oper={} #Dictionary of operations
    for o in [AND,COPY,LSHIFT,RSHIFT,NOT,OR]:
        oper[o.__name__]=o
    for inst in input:
        instQ.append(inst)
    while len(instQ)>0:
        i=instQ.pop(0) #Take first instruction from queue
        #print(i)
        gate=i.split(' -> ')[0]
        agn=True
        for v in gate.split(' '): #Check whether input wires have been assigned
            if v.islower() and v not in wires:
                agn=False
        if not agn: #If instruction is not ready, put it to the back of the queue
            instQ.append(i)
        else: #Enact instruction if ready
            op=list(filter(lambda x: x.isupper(),gate.split(' '))) #Find gate operator
            if len(op)==1:
                o=op[0]
            else:
                o='COPY' #Use copy if no operator specified
            vars=[]
            wOut=i.split(' -> ')[1]
            for v in gate.split(' '): #Pass wire values to gate
                if v.isnumeric():
                    vars.append(int(v))
                elif v.islower():
                    vars.append(wires[v])
            wires[wOut]=oper[o](*vars)
            print(len(instQ))
    return(wires)

retA=solveA(input)
            
            