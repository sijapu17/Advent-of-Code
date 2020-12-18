#Advent of Code 2020 Day 18

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-18.txt')
state = f.read()
input=[x.split() for x in state.replace('(',' ( ').replace(')',' ) ').splitlines()]

class Calculator(): #Calculator to perform arithmetic with alternative precedences

    def __init__(self,input):
        self.sums=[]
        for l in input: #Convert digits to int type
            sum=[]
            for x in l:
                if x.isdigit():
                    sum.append(int(x))
                else:
                    sum.append(x)
            self.sums.append(sum)

    def total_all_sums(self,part): #Find total of every sum
        ret=0
        for s in self.sums:
            if part==1:
                ret+=self.solve_sum(s)
            elif part==2:
                ret+=self.solve_sum_advanced(s)
        return(ret)

    def solve_sum(self,sum): #Solve a single sum (using left-to-right precendence)
        #If sum contains brackets, recurse to solve expression within brackets
        if '(' in sum or ')' in sum:
            lPos=sum.index('(') #Find position of first open bracket
            depth=1 #Bracket depth
            i=lPos
            for x in sum[lPos+1:]: #Find matching close bracket
                i+=1
                if x=='(':
                    depth+=1
                elif x==')':
                    depth-=1
                    if depth==0:
                        rPos=i
                        break

            return(self.solve_sum(sum[:lPos]+[self.solve_sum(sum[lPos+1:rPos])]+sum[rPos+1:])) #Recurse to solve section within outermost brackets
        #Once within all brackets, evaluate sum
        else:
            rev=sum[::-1] #Reverse sum to pop elements out from the end instead of start
            result=rev.pop() #Pop first element out
            while len(rev)>0:
                op=rev.pop()
                if op=='+':
                    result+=rev.pop()
                elif op=='*':
                    result*=rev.pop()
            return(result)

    def solve_sum_advanced(self,sum): #Solve a single sum (using advanced aritmetic giving precedence to add over mult)
        #If sum contains brackets, recurse to solve expression within brackets
        if '(' in sum or ')' in sum:
            lPos=sum.index('(') #Find position of first open bracket
            depth=1 #Bracket depth
            i=lPos
            for x in sum[lPos+1:]: #Find matching close bracket
                i+=1
                if x=='(':
                    depth+=1
                elif x==')':
                    depth-=1
                    if depth==0:
                        rPos=i
                        break

            return(self.solve_sum_advanced(sum[:lPos]+[self.solve_sum_advanced(sum[lPos+1:rPos])]+sum[rPos+1:])) #Recurse to solve section within outermost brackets
        #Once within all brackets, evaluate sum
        else:
            rev=sum[::-1] #Reverse sum to pop elements out from the end instead of start
            #Split expression into sums which can then be multiplied together
            interim=rev.pop() #Current sum
            result=1 #Total product
            while len(rev)>0:
                op=rev.pop()
                if op=='+': #Add to interim sum
                    interim+=rev.pop()
                elif op=='*': #Multiply interim onto result, reset interim
                    n=rev.pop()
                    result*=interim
                    interim=n
            result*=interim #Multiply final interim onto result
            return(result)

calc=Calculator(input)
print(calc.total_all_sums(1))
calc=Calculator(input)
print(calc.total_all_sums(2))