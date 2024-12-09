#Advent of Code 2024 Day 9

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2024/2024-09.txt')
input = f.read()

disk=[]
data=True
id=0
endlen=0

#Create disk
for d in input:
    for n in range(int(d)):
        if data:
            disk.append(id)
        else:
            disk.append('.')
    if data:
        id+=1
        endlen+=int(d)
    data=not data #Alternate between data and not data

def value(n):
    if n=='.':
        return(0)
    else:
        return(n)

#Fill gaps fully (Part 1)
def compact1(disk):
    index=0 #Index to start checking for gaps
    while index<endlen:
        if disk[index]!='.':
            index+=1
        else:
            disk[index]=disk.pop()
    #Remove any trailing gaps
    while disk[-1]=='.':
        disk.pop()
    return(sum([i*disk[i] for i in range(len(disk))]))

#Fill gaps without splitting packets (Part 2)
def compact2(disk:list):
    packetlens=input[::2] #Remove empty spaces to just keep lengths of packets
    for id, packlen in reversed(list(enumerate(packetlens))): #Iterate backwards through packets
        if id%500==0:
            print(id)
        packlen=int(packlen)
        oldloc=disk.index(id) #Location to move packet from
        for i in range(min(len(disk)-packlen,oldloc)): #Look for the first gap big enough to fit packet
            if disk[i:i+packlen]==['.']*packlen:
                for j in range(packlen):
                    disk[i+j]=id
                    disk[oldloc+j]='.'
                #print(''.join(str(x) for x in disk))
                break
    return(sum([i*value(disk[i]) for i in range(len(disk))]))

#print(compact1(disk))
#print(''.join(str(x) for x in disk))
print(compact2(disk))