#Advent of Code 2020 Day 3

import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-04.txt')
contents = f.read()
input=contents.splitlines()

class Records(): #Passport records

    def __init__(self,input): #Parse list of records
        self.recList=[]
        current={}
        for x in input:
            if len(x)==0: #At empty line, add current person to records and start new person
                self.recList.append(current)
                current={}
            else:
                line=x.split(' ') #Split line into list of fields
                for y in line:
                    current[y.split(':')[0]]=y.split(':')[1]
        self.recList.append(current) #Append final record

        self.p_ht=re.compile('^(\d+)(cm|in)$') #Height
        self.p_hr=re.compile('^#[0-9a-f]{6}$') #Hair
        self.p_ey=re.compile('^amb|blu|brn|gry|grn|hzl|oth$') #Eye
        self.p_pi=re.compile('^[0-9]{9}$') #PID

    def countValidA(self): #Count number of valid records (treating cid as optional)
        nValid=0
        reqFields=('byr','iyr','eyr','hgt','hcl','ecl','pid')
        for r in self.recList:
            valid=1
            for f in reqFields:
                if f not in r.keys(): #If any required field is not found, skip rest of fields and do not increment nValid
                    valid=0
                    break
            nValid+=valid
        return(nValid)

    def countValidB(self): #Count number of valid records (treating cid as optional and checking contents of fields)
        nValid=0
        reqFields=('byr','iyr','eyr','hgt','hcl','ecl','pid')
        for r in self.recList:
            valid=1
            for f in reqFields:
                if f not in r.keys(): #If any required field is not found, skip rest of fields and do not increment nValid
                    valid=0
                    break
                if not self.validField(f,r[f]):
                    valid=0
                    break
            nValid+=valid
        return(nValid)

    def validField(self,field,contents): #Checks field against its expected contents
        if field=='byr': #Check if birth year is 1920-2002
            return(int(contents) in range(1920,2003))

        elif field=='iyr': #Check if issue year is 2010-2020
            return(int(contents) in range(2010,2021))

        elif field=='eyr': #Check if expiry year is 2020-2030
            return(int(contents) in range(2020,2031))

        elif field=='hgt': #Check height in cm or inches
            m=re.match(self.p_ht,contents)
            if m is None:
                return(False) #If unit is incorrect, return false
            elif m.group(2)=='cm':
                return(int(m.group(1)) in range(150,194))
            elif m.group(2)=='in':
                return(int(m.group(1)) in range(59,77))
             
        elif field=='hcl': #Check against regex
            m=re.match(self.p_hr,contents)
            return(m is not None)

        elif field=='ecl': #Check against regex 
            m=re.match(self.p_ey,contents)
            return(m is not None)

        elif field=='pid': #Check against regex
            m=re.match(self.p_pi,contents)
            return(m is not None)

records=Records(input)
print(records.countValidA())
print(records.countValidB())