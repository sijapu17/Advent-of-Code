#Advent of Code 2023 Day 20

import re
from collections import defaultdict, deque
from math import prod

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2023/2023-20.txt')
contents = f.read()
input = contents.splitlines()
pattern1=re.compile('^(broadcaster|&\w+|%\w+) -> (.+)$')
modules={}
inputs=defaultdict(list)
signals=deque() #Queue of signals to be processed of the form (from_id,to_id,value)
pulses={True:0,False:0}
periods={}
presses=0

class Module():
    def __init__(self,line) -> None:
        m1=pattern1.match(line)
        if m1.group(1)=='broadcaster':
            self.id='broadcaster'
            self.type='broadcaster'
        else:
            self.type=m1.group(1)[0]
            self.id=m1.group(1)[1:]
        self.outputs=m1.group(2).split(', ')
        if self.type=='%': #Flip=flop module starts Off
            self.state=False
        #Log which modules have this module as an input
        for m in self.outputs:
            inputs[m].append(self.id)

        modules[self.id]=self

    def add_inputs(self):
        self.inputs={}
        for m in inputs[self.id]:
            self.inputs[m]=False #All inputs default to a low signal

    def process_signal(self,signal): #Process signal of the form (from_id,to_id,value)
        match self.type:
            case 'broadcaster':
                for m in self.outputs:
                    signals.append((self.id,m,signal[2]))
            case '%': #Flip-flop module
                if signal[2] is False:
                    self.state=not self.state #Flip state between True/False
                    for m in self.outputs:
                        signals.append((self.id,m,self.state))
            case '&': #Conjunction module
                self.inputs[signal[0]]=signal[2] #Update input memory
                signal_out=not all(self.inputs.values()) #If all inputs are high, output low - otherwise output high
                for m in self.outputs:
                    signals.append((self.id,m,signal_out))
        

    def __str__(self) -> str:
        return(f'M:{self.type}{self.id}')
    
    def __repr__(self) -> str:
        return(self.__str__())

#Initialise modules
def initialise():
    global modules
    global presses
    modules={}
    presses=0
    for l in input:
        Module(l)
    for m in modules.values():
        if m.type=='&': #Only conjunction modules need to keep track of input states
            m.add_inputs()

def process_signals(): #Process signal queue until empty
    global presses
    while len(signals)>0:
        signal=signals.popleft()
        pulses[signal[2]]+=1 #Count pulse
        if signal[1]==con and signal[2]==True:
            periods[signal[0]]=presses
        m=signal[1] #Module receiving signal
        if m in modules.keys():
            modules[m].process_signal(signal)

def press_button(): #Press button, sending low pulse to broadcaster, then process all resulting signals
    global presses
    signals.append(('button','broadcaster',False))
    presses+=1
    process_signals()

def count_pulses():
    for n in range(1000):
        press_button()
    return(pulses[True]*pulses[False])

#Find how many button presses it takes each of 4 inputs to send a high signal to con
def find_periods():
    while len(periods)<4:
        press_button()
    return(prod(periods.values()))
initialise()
#Find conjunction module which outputs to rx
for m in modules.values():
    if 'rx' in m.outputs:
        con=m.id
        break

#Part 1
print(count_pulses())

#Part 2
initialise()
print(find_periods()) #233099780262144 too low