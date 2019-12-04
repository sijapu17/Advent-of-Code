# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 09:06:33 2017

@author: Simon
"""

#Advent of Code 2017 Day 3

import math
input=361527

def side_length(number):
    side = math.ceil(math.sqrt(number))
    side = side if side % 2 != 0 else side + 1
    return side

#side = side_length(input)
#steps_to_reach_center_from_axis = (side-1)/2
#axises = [side**2 - ((side-1) * i)  - math.floor(side/2) for i in range(0, 4)] #get the axis "cells"
#steps_to_reach_axix_from_input = min([abs(axis - input) for axis in axises])

#print(steps_to_reach_axix_from_input + steps_to_reach_center_from_axis)


def coadd(a,b): #Add two coordinates together
    return(tuple([sum(x) for x in zip(a,b)]))

def solveB(input):

    grid={}
    grid[(0,0)]=1
    coord=(0,0) #Initial grid position
    step=0 #Total step
    rowstep=0 #Step in current row
    direction=[(1,0),(0,1),(-1,0),(0,-1)]
    diri=0 #Direction index
    sidelength=1
    maxval=0
    
    while (maxval<input):
        coord=coadd(coord,direction[diri])
        val=0
        for i in (-1,0,1):
            for j in (-1,0,1):
                nebr=coadd(coord,(i,j)) #Coordinates of a potential neighbour
                if nebr in grid:
                    val+=grid[nebr]
        grid[coord]=val
        maxval=max(val,maxval)
        step+=1
        rowstep+=1
        if rowstep==sidelength: #If corner is reached, turn anticlockwise
            rowstep=0
            diri=(diri+1)%4
            if diri%2==0: #For every other corner, increase sidelength by 1
                sidelength+=1
    return(maxval)
        
    
ret=solveB(input)