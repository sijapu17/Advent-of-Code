#Advent of Code 2020 Day 19

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-19.txt')
state = f.read()
input=state.splitlines()

class System():

    def __init__(self,input): #Parse rules and messages
        self.rules={}
        self.messages=[]
        for n in range(len(input)):
            line=input[n]
            if len(line)==0: #Stop checking at first empty line (end of rules section)
                break
            id=int(line.split(': ')[0])
            rule=[]
            for x in line.split(': ')[1].split():
                if x.isdigit():
                    rule.append(int(x))
                else:
                    rule.append(x.replace('"',''))
            self.rules[id]=rule
        
        for m in input[n+1:]:
            self.messages.append(m)


    def expand_rule(self,rule,part): #Whenever a number is found, recurse to replace it with its underlying rule
        if any(type(x)==int for x in rule): #If any numbers remain in rule, expand out
            pos=next(x for x, val in enumerate(rule) if type(val)==int) #Position of first number
            ruleID=rule[pos]
            if part==1:
                to_expand=self.rules[ruleID]
            elif part==2: #Special self-referential rules for 8 and 11
                if ruleID==8: #Match 42 one or more times
                    to_expand=[42,'+']
                elif ruleID==11: #Match 42 n times and then 31 n times (n>0)
                    to_expand=['(',42,31,')|(',42,42,31,31,')|(',42,42,42,31,31,31,')|(',42,42,42,42,31,31,31,31,')']
                else:
                    to_expand=self.rules[ruleID]
            return(self.expand_rule(rule[:pos] +['(']+ self.expand_rule(to_expand,part) +[')']+ rule[pos+1:],part))

        else:
            return(rule)

    def evaluate_rule(self,ID,part): #Turn expanded rule into regex and check how many messages follow rule
        expanded=self.expand_rule(self.rules[ID],part)
        reg=''.join(expanded).replace('(a)','a').replace('(b)','b') #Remove excess brackets for readibility
        pattern=re.compile('^('+reg+')$')
        valid=0 #Number of valid messages
        for m in self.messages:
            if pattern.search(m) is not None:
                valid+=1
        return(valid)

system=System(input)
print(system.evaluate_rule(0,1))
system=System(input)
print(system.evaluate_rule(0,2))