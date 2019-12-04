#Advent of Code 2018 Day 13

import math
import operator
from collections import deque
f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2018-13.txt')
contents = f.read()
input=contents.splitlines()
#input=['vvv','v||','|||']

def keyFromPos(dict,pos): #Return cart ID given pos
    for k, v in dict.items():
        if v.pos == pos:
            return(k)

def otherKeyFromPos(dict,id,pos): #Return cart ID given pos
    #print(str(id)+str(pos))
    for k, v in dict.items():
        if v.pos == pos and v.id != id and not v.crashed:
            #print('Other='+str(k))
            return(k)
        
class Mine(): #Overall class for mine containing map and carts
    
    def __init__(self,input): #Convert input into map and carts
        self.map={}
        self.carts={}
        self.w=len(input[0])
        self.h=len(input)
        self.crashes=0
        self.nCarts=0
        self.ticks=0
        self.occupiedCoords=set() #Keep track of which spots are occupied by carts
        
        id=0 #Incremental cart ID
        for j in range(self.h):
            for i in range(self.w):
                x=input[j][i]
                if x in ('<','^','>','v'):
                    pos=complex(i,j)
                    self.nCarts+=1
                    if x in ('<','>'): #Add in track hidden by cart
                        self.map[complex(i,j)]='-'
                    elif x in ('v','^'):
                        self.map[complex(i,j)]='|'
                    self.carts[id]=Cart(self,id,pos,x)
                    id+=1
                    self.occupiedCoords.add(pos)
                else:
                    self.map[complex(i,j)]=x
        print(str(self.nCarts)+' carts at start')

    def __str__(self):
        ret1='  '
        ret2='  '
        ret3=''
        for i in range(self.w):
            if i%10==0:
                ret1+=str(math.floor(abs(i)/10%10))
            else:
                ret1+=' '
            ret2+=str(abs(i)%10)
        for j in range(self.h):
            if j%10==0:
                ret3+=str(math.floor(abs(j)/10%10))
            else:
                ret3+=' '
            ret3+=str(abs(j)%10)
            for i in range(self.w):
                pos=complex(i,j)
                if pos in self.occupiedCoords:
                    id=keyFromPos(self.carts,pos) #Find cart in position
                    symbol=self.carts[id].symbol
                    ret3+=symbol
                else:
                    ret3+=self.map[pos]
            ret3+='\n'
        return(ret1+'\n'+ret2+'\n'+ret3)
    
    def runTick(self): #Move each cart once (in order) and determine crashes
        self.ticks+=1
        #print('Tick='+str(self.ticks))
        self.crashedIDs=set() #IDs of any carts that crash in tick
        coordOrder=sorted(self.occupiedCoords, key = lambda x : (x.imag,x.real)) #Sort carts by position in reading order
        cartOrder=[keyFromPos(self.carts,x) for x in coordOrder]
        #print('cartOrder='+str(cartOrder))
        for id in cartOrder:
            cart=self.carts[id]
            cart.moveCart()
        #print('Crashed IDs '+str(self.crashedIDs))
        for id in self.crashedIDs:
            del self.carts[id]
        self.occupiedCoords=set() #Reset occupiedCoords to only include non-crashed carts
        for c in self.carts.values():
            if not c.crashed:
                self.occupiedCoords.add(c.pos)
        self.nCarts=len(self.occupiedCoords)

            
    def crash(self,cart):
        print(str(self.nCarts)+' carts before crash')
        print('Crash at '+str(cart.pos))
        self.crashes+=1
        pos=cart.pos
        cart.crashed=True #Mark moving cart as crashed
        otherid=otherKeyFromPos(self.carts,cart.id,pos) #Find cart that was crashed into
        otherCart=self.carts[otherid]
        otherCart.crashed=True #Mark other cart as crashed
        self.occupiedCoords.remove(cart.pos) #Remove from list so future carts do not crash
        self.crashedIDs.add(cart.id)
        self.crashedIDs.add(otherid)

class Cart():
    
    def __init__(self,mine,id,pos,symbol):
        self.mine=mine
        self.id=id
        self.pos=pos
        self.symbol=symbol
        self.crashed=False
        self.turnSeq=deque([complex(0,-1),complex(1,0),complex(0,1)])
        self.dirCycle=deque([complex(-1,0),complex(0,-1),complex(1,0),complex(0,1)])
        self.symCycle=deque(['<','^','>','v'])
        while self.symbol!=self.symCycle[0]: #Initialise direction cycle to correct start point
            self.symCycle.rotate()
            self.dirCycle.rotate()
        self.dir=self.dirCycle[0]

    def turnCart(self,dir): #Turn cart given direction
        self.dir*=dir
        while self.dir!=self.dirCycle[0]: #Rotate dirCycle and symCycle to correct point
            self.symCycle.rotate()
            self.dirCycle.rotate()
        self.symbol=self.symCycle[0]
        
    def turnCartAtIntersection(self):
        self.turnCart(self.turnSeq[0])
        self.turnSeq.rotate(-1)


    def turnCartAtCorner(self,corner):
        if corner=='/':
            factor=-1
        elif corner=='\\': #Extra backslash is escape char
            factor=1
        dir=self.dir
        if dir.real!=0:
            turn=complex(0,1)*factor
        else:
            turn=complex(0,-1)*factor
        self.turnCart(turn)
        
            
        
    def moveCart(self): #Move cart one step forward, then turn if required
        
        #print(str(self.id)+str(self.crashed))
        if not self.crashed: #If cart has already been crashed into, do not move it
            self.mine.occupiedCoords.remove(self.pos)
            self.pos+=self.dir #Move forward one space
            if self.pos in self.mine.occupiedCoords:
                self.mine.crash(self)               
            else:
                self.mine.occupiedCoords.add(self.pos)
                track=self.mine.map[self.pos] #Find track type underneath cart
                if track=='+':
                    self.turnCartAtIntersection()
                elif track in {'/','\\'}:
                    self.turnCartAtCorner(track)

def solveA(input):
    mine=Mine(input)
    while mine.crashes==0:
        mine.runTick()
        
#retA=solveA(input)

def solveB(input):
    mine=Mine(input)
    while mine.nCarts>1:# and ticks<341:
        if mine.ticks%1000==1 or mine.nCarts==5:
            print('Tick='+str(mine.ticks)+' '+str(mine.nCarts)+' carts remaining')
        #if mine.ticks in set([1357,1358]):
        #print(mine.carts)
        #print(mine)    
        mine.runTick()
    return(mine)
    print(mine)
    #return(mine.occupiedCoords)
        
retB=solveB(input)