#Advent of Code 2015 Day 14b

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2015-14.txt')
contents = f.read()
input = contents.splitlines()

class Deer():
    def __init__(self,line):
        words=line.split(' ')
        self.name=words[0]
        self.score=0
        self.speed=int(words[3])
        self.fTime=int(words[6]) #Flying time
        self.rTime=int(words[13]) #Rest time
        self.cycTime=self.fTime+self.rTime #Time for full cycle
        
    def getDist(self,time):
        self.cycles=time//self.cycTime #Number of full cycles achieved
        self.endTime=min(time%self.cycTime,self.fTime) #TIme for partial cycle at end of race
        self.totFTime=self.cycles*self.fTime+self.endTime
        self.dist=self.speed*self.totFTime
        return(self.dist)
        
def impPack(input):
    pack={} #Dict of all reindeer
    for deer in input:
        name=deer.split(' ')[0]
        pack[name]=Deer(deer)
    return(pack)

pack=impPack(input)

def solveB(pack,time):
    for t in range(time):
        dists={}
        for name, deer in pack.items():
            dists[name]=deer.getDist(t+1) #Start scoring at time t+1
        mDist=max(dists.values())
        for name, dist in dists.items(): #If deer is in the (joint) lead at time t, +=1 point
            if dist==mDist:
                pack[name].score+=1
    points={} #Find max points at end
    for name, deer in pack.items():
        points[name]=deer.score
    mx=max(points.values())
    for name, deer in pack.items(): #Print scores
        print(name+': '+str(deer.score)+' points')
    return(mx)       

retB=solveB(pack,2503)