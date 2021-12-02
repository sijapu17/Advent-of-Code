#Advent of Code 2021 Day 1

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-02.txt')
contents = f.read()
input = contents.splitlines()

def solveA(input):
    h, d = 0, 0 #Initialise height and depth to 0
    for i in input:
        inst=i.split()[0] #Instruction type
        mag=int(i.split()[1]) #Instruction magnitude
        if inst=='forward':
            h+=mag
        elif inst=='up':
            d-=mag
        elif inst=='down':
            d+=mag

    print('Height={0}, Depth={1}'.format(h,d))
    return(h*d)

retA=solveA(input)
print(retA)    

def solveB(input):
    h, d, a = 0, 0, 0 #Initialise height, depth and aim to 0
    for i in input:
        inst=i.split()[0] #Instruction type
        mag=int(i.split()[1]) #Instruction magnitude
        if inst=='forward':
            h+=mag
            d+=mag*a #Increase depth by mag multiplied by aim
        elif inst=='up':
            a-=mag
        elif inst=='down':
            a+=mag

    print('Height={0}, Depth={1}, Aim={2}'.format(h,d,a))
    return(h*d)

retB=solveB(input)
print(retB)  