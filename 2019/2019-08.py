#Advent of Code 2019 Day 8

from collections import defaultdict

f = open('C:/Users/Simon/SkyDrive/Home Stuff/Python/Advent of Code/2019/2019-08.txt')
contents = f.read()
input=[int(x) for x in list(contents)]

width=25
height=6

def solveA(input,width,height): #Find the layer with fewest zeroes, and count number of 1s and 2s in that layer
    layerSize=width*height
    i=0
    counts=defaultdict(lambda : defaultdict(int)) #Count of instances of digits by layer number
    for d in input:
        layer=i//layerSize #Work out which layer a given pixel is on
        counts[layer][d]+=1
        i+=1
    minLayer=min(counts, key=lambda x:counts[x][0]) #Find layer with fewest zeroes
    checksum=counts[minLayer][1]*counts[minLayer][2]
    return(checksum)

#retA=solveA(input,width,height)

def decodeImage(input,width,height): #Create coordinate dictionary with first non-transparent pixel in each position
    layerSize=width*height
    image=dict()
    for h in range(height):
        for w in range(width):
            pos=h*width+w
            while True:
                if input[pos]<2: #If position on layer is non-transparent, save to image
                    image[complex(w,h)]=input[pos]
                    break
                pos+=layerSize #If not, move to same position on next layer back
    return(image)
    
image=decodeImage(input, width,height)
    
def displayImage(image,width,height): #Display ASCII version of image
    font={0:'.', 1:'#'} #Convert 1 and 0 to 'black' and 'white'
    for h in range(height):
        line=''
        for w in range(width):
            line+=font[image[complex(w,h)]]
        print(line)

displayImage(image, width,height)
    
    