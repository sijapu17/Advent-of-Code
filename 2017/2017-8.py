# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 21:54:55 2017

@author: Simon
"""

#Advent of Code 2017 Day 8

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2017-8.txt')
contents = f.read()
file_as_list = contents.splitlines()

class Instruction():
    def __init__(self,line):
        self.line=line
        split=self.line.split()
        self.convar=split[4]
        self.conop=split[5]
        self.conval=int(split[6])
        self.insvar=split[0]
        if split[1]=='inc':
            self.insval=int(split[2])
        elif split[1]=='dec':
            self.insval=-int(split[2])
            
    def __str__(self):
        return(self.line)
        
def importList(input):
    list=[]
    for l in input:
        list.append(Instruction(l))
    return list

input=importList(file_as_list)
    
def solveA(input):
    reg={} #Registry of all variables and their values
    for inst in input:
        if inst.convar not in reg: #Initialise variable to 0 if new
            reg[inst.convar]=0
        if inst.insvar not in reg: #Initialise variable to 0 if new
            reg[inst.insvar]=0
        #Check whether condition is true
        cond=0
        if inst.conop=='==':
            if reg[inst.convar]==inst.conval:
                cond=1
        elif inst.conop=='!=':
            if reg[inst.convar]!=inst.conval:
                cond=1            
        elif inst.conop=='<':
            if reg[inst.convar]<inst.conval:
                cond=1
        elif inst.conop=='<=':
            if reg[inst.convar]<=inst.conval:
                cond=1
        elif inst.conop=='>':
            if reg[inst.convar]>inst.conval:
                cond=1
        elif inst.conop=='>=':
            if reg[inst.convar]>=inst.conval:
                cond=1
        else:
            print('Warning: Operation '+inst.conop+' not recognised')
        #Carry out instruction if condition is true
        if cond==1:
            reg[inst.insvar]+=inst.insval
    mx=max(iter(reg.values()))
    return(mx)

#retA=solveA(input)
#xx=iter(x.values())
#y=max(xx)

def solveB(input):
    reg={} #Registry of all variables and their values
    highest=0
    for inst in input:
        if inst.convar not in reg: #Initialise variable to 0 if new
            reg[inst.convar]=0
        if inst.insvar not in reg: #Initialise variable to 0 if new
            reg[inst.insvar]=0
        #Check whether condition is true
        cond=0
        if inst.conop=='==':
            if reg[inst.convar]==inst.conval:
                cond=1
        elif inst.conop=='!=':
            if reg[inst.convar]!=inst.conval:
                cond=1            
        elif inst.conop=='<':
            if reg[inst.convar]<inst.conval:
                cond=1
        elif inst.conop=='<=':
            if reg[inst.convar]<=inst.conval:
                cond=1
        elif inst.conop=='>':
            if reg[inst.convar]>inst.conval:
                cond=1
        elif inst.conop=='>=':
            if reg[inst.convar]>=inst.conval:
                cond=1
        else:
            print('Warning: Operation '+inst.conop+' not recognised')
        #Carry out instruction if condition is true
        if cond==1:
            reg[inst.insvar]+=inst.insval
            linemx=max(iter(reg.values()))
            highest=max(highest,linemx)
    return(highest)
    
retB=solveB(input)