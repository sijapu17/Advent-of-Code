#import numpy as np

BIG_NUM = 1000000  # try larger numbers until solution found

goal = 33100000
#houses_a = np.zeros(BIG_NUM)
houses_b = [0]*BIG_NUM

for elf in range(1, BIG_NUM):
    #houses_a[elf::elf] += 10 * elf
    houses_b[elf:(elf+1)*50:elf] +=11*elf

#print(np.nonzero(houses_a >= goal)[0][0])
#print(np.nonzero(houses_b >= goal)[0][0])