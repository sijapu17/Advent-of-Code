#Advent of Code 2015 Day 14

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2015-14.txt')
contents = f.read()
input = contents.splitlines()

class Deer():
    def __init__(self,line,time):
        words=line.split(' ')
        self.name=words[0]
        self.speed=int(words[3])
        self.fTime=int(words[6]) #Flying time
        self.rTime=int(words[13]) #Rest time
        self.cycTime=self.fTime+self.rTime #Time for full cycle
        self.cycles=time//self.cycTime #Number of full cycles achieved
        self.endTime=min(time%self.cycTime,self.fTime) #TIme for partial cycle at end of race
        self.totFTime=self.cycles*self.fTime+self.endTime
        self.dist=self.speed*self.totFTime
        
def impPack(input,time):
    pack={} #Dict of all reindeer
    for deer in input:
        name=deer.split(' ')[0]
        pack[name]=Deer(deer,time)
    return(pack)

pack=impPack(input,2503)

def solveA(pack):
    mDist=0
    mDeer=None
    for deer in pack.values():
        print(deer.name+' '+str(deer.dist))
        if deer.dist>mDist:
            mDist=deer.dist
            mDeer=deer.name
    return([mDeer,mDist])       

retA=solveA(pack)