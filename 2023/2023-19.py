#Advent of Code 2023 Day 19

import re
from itertools import product

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-19.txt')
contents = f.read()
input = contents.splitlines()
pattern1=re.compile('(\w+){(.+)}')
pattern2=re.compile('(\w)([<>])(\d+):(\w+)')
pattern3=re.compile('{x=(\d+),m=(\d+),a=(\d+),s=(\d+)')


def comp(y,dir,a): #Returns True/False for y<a or y>a
    if dir=='<':
        return(y<a)
    elif dir=='>':
        return(y>a)
    
def comp_range(r,dir,a): #Splits a range into (range where True, range where False) based on comparison
    if dir=='<':
        if r[1]<a: #Whole range below comparator
            return((r,None))
        elif r[0]<a<=r[1]: #Comparator within range
            return((r[0],a-1),(a,r[1]))
        elif a<=r[0]: #Whole range above comparator
            return((None,r))
        else:
            return('No condition met')
    elif dir=='>':
        if r[0]>a: #Whole range above comparator
            return((r,None))
        elif r[0]<=a<r[1]: #Comparator within range
            return((a+1,r[1]),(r[0],a))
        elif r[1]<=a: #Whole range below comparator
            return((None,r))
        else:
            return('No condition met')        



def send_to_workflow(part,dest):
    global next_workflow
    global to_process
    global total_rating
    if dest=='A': #Accepted parts
        to_process-=1
        total_rating+=part.rating
        next_workflow='in'
    elif dest=='R':
        to_process-=1
        next_workflow='in'
    else:
        workflows[dest].queue.append(part)
        next_workflow=dest

def send_to_workflow_range(part,dest):
    global accepted_parts
    #print(f'{dest} {part}')
    if dest=='A':
        accepted_parts.append(part)
    elif dest!='R':
        workflows[dest].queue.append(part)
        to_visit.append(dest)

class Workflow():
    def __init__(self,name,rules) -> None:
        self.name=name
        self.rules=[] #List of rules
        for r in rules.split(',')[:-1]:
            m=pattern2.match(r)
            self.rules.append((m.group(1),m.group(2),int(m.group(3)),m.group(4)))
        self.backstop=rules.split(',')[-1] #Destination if all rules fail
        self.queue=[] #Queue of parts waiting to be evaluated by this workflow

    def eval_part(self): #Evaluate next part from queue
        part=self.queue.pop()
        for r in self.rules: #Check each rule in order
            if comp(part.val(r[0]),r[1],r[2]):
                send_to_workflow(part,r[3])
                return
        send_to_workflow(part,self.backstop)

    def eval_part_range(self): #Evaluate next range part from queue
        part=self.queue.pop()
        for r in self.rules: #Check each rule in order
            range_t, range_f=comp_range(part.val(r[0]),r[1],r[2])
            #Send section of part that passes rule to new destination
            if range_t is not None:
                send_to_workflow_range(part.create_new(r[0],range_t),r[3])
            #Send section of part that fails rule onto next rule in workflow
            if range_f is None: #End workflow if no range failed
                return
            part=part.create_new(r[0],range_f)
        send_to_workflow_range(part,self.backstop)

class Part():
    def __init__(self,x,m,a,s) -> None:
        self.x=x
        self.m=m
        self.a=a
        self.s=s
        if type(x)==int:
            self.rating=x+m+a+s

    def __str__(self) -> str:
        return(f'Part({self.x},{self.m},{self.a},{self.s})')
    
    def __repr__(self) -> str:
        return(self.__str__())

    def val(self,p:str): #Return value of given property
        match p:
            case 'x':
                return(self.x)
            case 'm':
                return(self.m)
            case 'a':
                return(self.a)
            case 's':
                return(self.s)
            
    def create_new(self,p:str,range): #Create new part which is a copy of existing part, except for property p which has new range
        match p:
            case 'x':
                return(Part(range,self.m,self.a,self.s))
            case 'm':
                return(Part(self.x,range,self.a,self.s))
            case 'a':
                return(Part(self.x,self.m,range,self.s))
            case 's':
                return(Part(self.x,self.m,self.a,range))

to_process=0 #Count number of parts still in workflows
total_rating=0
workflows={} #Dictionary of workflows
next_workflow='in'

i=-1
while True: #Create workflows
    i+=1
    if len(input[i])==0:
        break
    m=pattern1.match(input[i])
    workflows[m.group(1)]=Workflow(m.group(1),m.group(2))
while i<len(input)-1: #Create parts
    i+=1
    m=pattern3.match(input[i])
    part=Part(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)))
    send_to_workflow(part,'in') #All parts start at workflow 'in'
    to_process+=1
    
#Process parts
while to_process>0:
    workflows[next_workflow].eval_part()

print(total_rating)

#Part 2: Assess all combinations
accepted_parts=[]
to_visit=[] #List of workflows to visit
part=Part((1,4000),(1,4000),(1,4000),(1,4000))
send_to_workflow_range(part,'in')

#Process parts
while len(to_visit)>0:
    next_workflow_2=to_visit.pop()
    workflows[next_workflow_2].eval_part_range()

total_parts=0
for p in accepted_parts:
    total_parts+=(p.x[1]-p.x[0]+1)*(p.m[1]-p.m[0]+1)*(p.a[1]-p.a[0]+1)*(p.s[1]-p.s[0]+1)
print(total_parts)