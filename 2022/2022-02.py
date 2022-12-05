#Advent of Code 2022 Day 2

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2022/2022-02.txt')
contents = f.read()
input = contents.splitlines()

def get_score_1(i,j): #i=Opponent shape, j=Player shape
    res=(ord(j)-ord(i)+2)%3 #2=win, 1=draw, 0=loss
    shape=ord(j)-87 #1=rock, 2=paper=, 3=scissors
    return(res*3+shape)
   
def get_score_2(i,j): #i=Opponent shape, j=Desired result
    offset=(ord(j)-86)%3 #2=loss, 0=draw, 1=win
    shape=(ord(i)-64+offset)%3
    if shape==0:
        shape+=3
    res=(ord(j)-88)*3
    #print(f'Result {res} Shape {shape}')
    #print(res+shape)
    return(res+shape)
   
def run_matches(input,part): #Loop through all matches and sum total score
    total=0
    for x in input:
        if part==1:
            total+=get_score_1(x[0],x[2])
        elif part==2:
            total+=get_score_2(x[0],x[2])
    return(total)
       
print(run_matches(input,1))
print(run_matches(input,2))