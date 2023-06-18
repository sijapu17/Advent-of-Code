#Advent of Code 2022 Day 25

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-25.txt')
contents = f.read()
input = contents.splitlines()

#Convert a SNAFU number into decimal
def snafu_to_decimal(snafu_in:str):
    digits={'=':-2,'-':-1,'0':0,'1':1,'2':2}
    sum=0
    mul=1
    for d in reversed(snafu_in):
        sum+=digits[d]*mul
        mul*=5
    return(sum)

#Convert a decimal number into SNAFU
def decimal_to_snafu(dec_in:int):
    digits={'=':-2,'-':-1,'0':0,'1':1,'2':2}
    snafu_out=[]
    dec_so_far=0 #Decimal representation of intermediate snafu number
    exp=0 #Exponent for power of 5
    while True:
        #Loop to find the snafu digit at exponent exp so number differs from dec_in by a multiple of exp+1
        for s,d in digits.items():
            dec_test=dec_so_far+d*(5**exp)
            diff=dec_in-dec_test
            if diff%5**(exp+1) == 0:
                snafu_out.insert(0,s)
                dec_so_far=dec_test
                if dec_so_far==dec_in:
                    return(''.join(snafu_out))
                exp+=1
                break

print(decimal_to_snafu(sum([snafu_to_decimal(x) for x in input])))