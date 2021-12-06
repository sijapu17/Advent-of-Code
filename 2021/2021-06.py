from collections import deque
inp=[5,1,1,1,3,5,1,1,1,1,5,3,1,1,3,1,1,1,4,1,1,1,1,1,2,4,3,4,1,5,3,4,1,1,5,1,2,1,1,2,1,1,2,1,1,4,2,3,2,1,4,1,1,4,2,1,4,5,5,1,1,1,1,1,2,1,1,1,2,1,5,5,1,1,4,4,5,1,1,1,3,1,5,1,2,1,5,1,4,1,3,2,4,2,1,1,4,1,1,1,1,4,1,1,1,1,1,3,5,4,1,1,3,1,1,1,2,1,1,1,1,5,1,1,1,4,1,4,1,1,1,1,1,2,1,1,5,1,2,1,1,2,1,1,2,4,1,1,5,1,3,4,1,2,4,1,1,1,1,1,4,1,1,4,2,2,1,5,1,4,1,1,5,1,1,5,5,1,1,1,1,1,5,2,1,3,3,1,1,1,3,2,4,5,1,2,1,5,1,4,1,5,1,1,1,1,1,1,4,3,1,1,3,3,1,4,5,1,1,4,1,4,3,4,1,1,1,2,2,1,2,5,1,1,3,5,2,1,1,1,1,1,1,1,4,4,1,5,4,1,1,1,1,1,2,1,2,1,5,1,1,3,1,1,1,1,1,1,1,1,1,1,2,1,3,1,5,3,3,1,1,2,4,4,1,1,2,1,1,3,1,1,1,1,2,3,4,1,1,2]

def run_day(fish): #Run 1 day of simulation
    parents=fish.popleft() #Fish at position 0 become parents and leave the queue, all other fish move one position to the left
    fish[-2]+=parents #Parents reset to position 6
    fish.append(parents) #Equal nummber of children added to position 8
    return(fish)
    
def run_n_days(n): #Run n days of simulation and return total number of fish
    fish=deque([inp.count(i) for i in range(9)])
    for i in range(n):
        run_day(fish)
    print(fish)
    return(sum([x for x in fish]))

import time

start=time.perf_counter() #Test speed of code run
print(run_n_days(80)) #Part 1
mid=time.perf_counter()-start
print('Part 1 took {} seconds'.format(mid))
print(run_n_days(256)) #Part 2
end=time.perf_counter()-mid
print('Part 2 took {} seconds'.format(end))