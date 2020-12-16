#Advent of Code 2020 Day 16

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-16.txt')
contents = f.read()
input=contents.splitlines()

class System():

    def __init__(self,input):
        p1=re.compile('(^.+): (\d+)\-(\d+) or (\d+)\-(\d+)$')
        self.valid=set()
        self.fields={}
        for n in range(len(input)):
            if len(input[n])==0: #Stop checking at first empty line (end of rules section)
                break
            m=re.match(p1,input[n])
            #Add field to dict of fields
            self.fields[m.group(1)]={}
            self.fields[m.group(1)]['vals']=set()
            #Add ranges to set of valid ints
            for i in range(int(m.group(2)),int(m.group(3))+1):
                self.valid.add(i)
                self.fields[m.group(1)]['vals'].add(i)
            for i in range(int(m.group(4)),int(m.group(5))+1):
                self.valid.add(i)
                self.fields[m.group(1)]['vals'].add(i)

        #Add range of numbers equal to number of fields to each field, to indicate possible positions of field on the tickets
        for f in self.fields.keys():
            self.fields[f]['pos']=set(range(n))

        self.my_ticket=[int(x) for x in input[n+2].split(',')] #My ticket is 2 lines after end of rules
        self.nearby_tickets=[]
        for l in input[n+5:]: #Nearby tickets start 5 lines after end of rules
            self.nearby_tickets.append([int(x) for x in l.split(',')])
        pass
        
    def count_invalid_fields(self): #Sum all field values which are not in valid range for any field
        count=0
        for l in self.nearby_tickets:
            for v in l:
                if v not in self.valid:
                    count+=v
        return(count)

    def discard_invalid_tickets(self): #Discard tickets with any field values which are not in valid range for any field
        valid_tickets=[]
        for l in self.nearby_tickets:
            valid=True #Initialise to true, change to false if any invalid value found
            for v in l:
                if v not in self.valid:
                    valid=False
            if valid:
                valid_tickets.append(l)
        self.nearby_tickets=valid_tickets #Replace original list with reduced list

    def match_fields_to_pos(self): #Work out which field relates to which pos
        
        self.discard_invalid_tickets() #Remove all invalid tickets
        for t in self.nearby_tickets:
            for pos in range(len(t)):
                for f in self.fields.keys():
                    #If value at pos on current ticket is not in valid range for a field, we can remove that pos as a possibility
                    if pos in self.fields[f]['pos'] and t[pos] not in self.fields[f]['vals']:
                        self.fields[f]['pos'].remove(pos)

        fields=[] #Simplify fields now value ranges are no longer needed
        for f in self.fields.keys():
            fields.append((f,self.fields[f]['pos']))
        fields.sort(reverse=True,key=lambda x: len(x[1])) #Sort by number of possible positions
        
        ret=1 #Return value, i.e. product of fields containing word 'departure'
        while len(fields)>0:
            x=fields.pop() #Remove last field from list (which should have 1 pos)
            pos=x[1].pop() #Remove pos from size 1 set
            for f in fields: #Remove pos as option from other fields
                if pos in f[1]:
                    f[1].remove(pos)

            if x[0].find('departure')>=0:
                ret*=self.my_ticket[pos]
        
        return(ret)
                

system=System(input)
print(system.count_invalid_fields())
print(system.match_fields_to_pos())