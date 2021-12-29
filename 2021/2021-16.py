#Advent of Code 2021 Day 16

from functools import reduce
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-16.txt')
inp = f.read()

def hex2bin(hex): #Convert hexadecimal value to binary string of 1/0
    ret=''
    for x in hex:
        dec=int(x,16)
        ret+=f"{dec:04b}"
    return(ret)

class Packet():
    def __init__(self,version,type,data) -> None:
        global version_sum
        self.version=version
        version_sum+=version
        self.type=type
        self.data=data #Data may be a literal or an operator packet

    def __repr__(self) -> str:
        return(f'V{self.version}T{self.type} {{{self.data}}}')

    def __str__(self) -> str:
        return(self.__repr__())

    def evaluate(self): #Evaluate packet, using recursion if there are sub-packets
        if self.type==4: #Literal
            return(self.data)
        else:
            data_eval=[x.evaluate() for x in self.data] #Recursively evaluate all sub-packets
            if self.type==0: #Sum
                return(sum(data_eval))
            elif self.type==1: #Product
                return(reduce((lambda x, y: x * y), data_eval))
            elif self.type==2: #Minimum
                return(min(data_eval))
            elif self.type==3: #Maximum
                return(max(data_eval))
            elif self.type==5: #>
                return(int(data_eval[0]>data_eval[1]))
            elif self.type==6: #<
                return(int(data_eval[0]<data_eval[1]))
            elif self.type==7: #==
                return(int(data_eval[0]==data_eval[1]))

def extract_packets(bin_str:str,packets:list,last_pos=-1,n_packets_req=-1,level=0): #Extract all packets from a binary string and put them in list
    global pos
    if last_pos==-1:
        last_pos=len(bin_str)
    while len(packets)!=n_packets_req and pos<last_pos: #Carry on to end, ignoring up to three zeroes at end which may be a spare partial hex value
        #Read version and type from start of string
        version=int(bin_str[pos:pos+3],2)
        pos+=3
        type=int(bin_str[pos:pos+3],2)
        pos+=3
        if type==4: #For literal data, read string in chunks of 5 bits, where first bit of each chunk is 'last chunk' indicator
            bin_data=''
            while True:
                bin_data+=bin_str[pos+1:pos+5]
                pos+=5
                if bin_str[pos-5]=='0': #Indicator that this is last chunk of data
                    break
            data=int(bin_data,2)
            packets.append(Packet(version,type,data))
        else: #For operator data, process data depending on length type ID
            ltID=bin_str[pos]
            pos+=1
            data=[]
            if ltID=='0': #The next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet
                bitlength=int(bin_str[pos:pos+15],2)
                pos+=15
                extract_packets(bin_str,data,last_pos=pos+bitlength,level=level+1) #Recursively add sub-packets
            elif ltID=='1': #the next 11 bits are a number that represents the number of sub-packets immediately contained by this packet
                n_packets=int(bin_str[pos:pos+11],2)
                pos+=11
                extract_packets(bin_str,data,n_packets_req=n_packets,level=level+1) #Recursively add sub-packets
            packets.append(Packet(version,type,data))

packets=[]
bininp=hex2bin(inp)
version_sum=0
pos=0
extract_packets(bininp,packets,n_packets_req=1)
packet=packets[0] #Top level is always a single packet
print(packet)
print(f'Version sum = {version_sum}')
print(f'Result = {packet.evaluate()}')
