#Advent of Code 2015 Day 25
#Find number on row 3010, column 3019

def findStep(r,c):
    maxRow=1
    n=1
    row=1
    col=1
    while True:
        n+=1
        row-=1
        col+=1
        if row==0:
            col=1
            maxRow+=1
            row=maxRow
            #print(str(n)+': Row '+str(row)+' Col '+str(col))
        #if row>3000 and col>3000:
            #print(str(n)+': Row '+str(row)+' Col '+str(col))
        if r==row and c==col:
            return(n)
        
#step=findStep(3010,3019)
step=18168397
        
def genCode(n):
    i=20151125
    m=252533
    d=33554393
    for x in range(n-1):
        if x%1000000==1:
            print('Step '+str(x))
        i=(i*m)%d
    return(i)

resA=genCode(step)