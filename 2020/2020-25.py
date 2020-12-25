#Advent of Code 2020 Day 25

keys=(9717666,20089533)
#keys=(5764801,17807724) #Example input

def find_cycle(public): #Find cycle number of public key by trial and error
    x=1 #Value
    n=0 #Cycle number
    while True:
        if x==public:
            print(n)
            return(n)
        n+=1
        x*=7
        x=x%20201227

cycles=[find_cycle(x) for x in keys] #(17167199,19814867)

print(pow(keys[0],cycles[1],20201227))
