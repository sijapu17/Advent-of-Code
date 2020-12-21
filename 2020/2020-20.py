#Advent of Code 2020 Day 20

import re
from collections import deque

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2020/2020-20.txt')
state = f.read()
input=state.splitlines()

def get_edgeID(edge): #Convert string of #/. into a binary number
    bin_str=edge.replace('#','1').replace('.','0')
    mul=1
    if bin_str[::-1]<bin_str: #Keep lowest of the two possible strings
        mul=-1
    out=min(bin_str[::-1],bin_str) #Use smaller ID out of edge and reflected edge
    return(mul*int(out,base=2))

class Square(): #Class used for tiles and full image

    def __init__(self):
        self.dim=1 #Placeholder

    def reflect(self,IDs=True): #Reflect tile across y-axis
        new={}
        #Remap pixel coordinates
        for k,v in self.pixels.items():
            new[complex(k.real,self.dim-1-k.imag)]=v
        self.pixels=new
        if IDs:
        #Remap edgeIDs
            order=[self.edgeIDs_ordered[2],self.edgeIDs_ordered[1],self.edgeIDs_ordered[0],self.edgeIDs_ordered[3]]
            self.edgeIDs_ordered=[(-1*x) for x in order] #Reverse all IDs

    def rotate(self,IDs=True): #Rotate tile clockwise
        new={}
        #Remap pixel coordinates
        for k,v in self.pixels.items():
            new[complex(self.dim-1-k.imag,k.real)]=v
        self.pixels=new
        if IDs:
        #Remap edgeIDs
            order=[self.edgeIDs_ordered[1],self.edgeIDs_ordered[2],self.edgeIDs_ordered[3],self.edgeIDs_ordered[0]]
            self.edgeIDs_ordered=order

class Image(Square): #Full image

    def __init__(self,pixels):
        self.pixels=pixels
        #Find bounds of pixels
        minX=int(min(self.pixels.keys(),key=lambda x:x.real).real)
        maxX=int(max(self.pixels.keys(),key=lambda x:x.real).real)      
        self.dim=maxX-minX+1
        self.hash_size=sum(x=='#' for x in self.pixels.values())  #Number of hash symbols in image

    def __str__(self): #Print tile
        ret=''
        for j in range(self.dim):
            for i in range(self.dim):
                ret+=self.pixels[complex(i,j)]
            ret+='\n'
        return(ret) 

class Tile(Square): #Single 10x10 tile
    def __init__(self,lines,ID):
        self.tileID=ID
        self.dim=len(lines)
        self.pixels={} #Key=coord, Val=#/.
        for j in range(self.dim):
            for i in range(self.dim):
                self.pixels[complex(i,j)]=lines[j][i]
        self.lines=lines
        self.edgeIDs=set()
        self.edgeIDs_ordered=[]
        #Add four edges into edgeIDs (Initial top, left, bottom, right)
        edges=[self.lines[0],''.join([x[0] for x in self.lines][::-1]),self.lines[9][::-1],''.join([x[9] for x in self.lines])]
        for e in edges:
            self.edgeIDs.add(abs(get_edgeID(e))) #Unordered edges for initial tile matching
            self.edgeIDs_ordered.append(get_edgeID(e)) #Ordered edges for working out correct orientations

    def __str__(self): #Print tile
        ret='Tile '+str(self.tileID)+':\n  '+str(self.edgeIDs_ordered[0])+'\n'+str(self.edgeIDs_ordered[1])+' '+str(self.edgeIDs_ordered[3])+'\n  '+str(self.edgeIDs_ordered[2])+'\n'
        for j in range(self.dim):
            for i in range(self.dim):
                ret+=self.pixels[complex(i,j)]
            ret+='\n'
        return(ret)        
        
    def shared_edge(self,other): #Check whether two tiles share a matching edge, returns edgeID if so
        shared=self.edgeIDs & other.edgeIDs
        if len(shared)>0:
            return(shared.pop())
        return(None)

    def orient_to_match(self,edgeID,side=1): #Reflect/rotate until the specified tile side joins with the given edgeID (i.e. they add to 0)
        if edgeID in self.edgeIDs_ordered: #If tile has an edgeID that matches the other edgeID, reflect tile to reverse edge direction
            self.reflect()
        while self.edgeIDs_ordered[side]!=-1*edgeID: #Rotate until desired side joins to edgeID
            self.rotate()

class System(): #Array of tiles to be joined into the full image
    def __init__(self,input):
        self.tiles={}
        self.inner_edgeIDs=set() #Set of inner edgeIDs (i.e. those that match another tile)
        current=[]
        i=0
        while i<len(input):
            line=input[i]
            if 'Tile' in line: #Get tile ID number
                ID=int(line[5:-1])
            elif len(line)>0:
                current.append(line)
            else: #Start new tile
                self.tiles[ID]=Tile(current,ID)
                current=[]
            i+=1
        self.tiles[ID]=Tile(current,ID) #Add final tile
        self.dim=int(len(self.tiles)**0.5)

        monster=['                  # ','#    ##    ##    ###',' #  #  #  #  #  #   ']
        self.mon_length=len(monster[0])
        self.mon_height=len(monster)
        self.monster=set() #Create set of relative monster coordinates
        for j in range(self.mon_height):
            for i in range(self.mon_length):
                if monster[j][i]=='#':
                    self.monster.add(complex(i,j))
        self.mon_size=len(self.monster) #Number of hashes in monster

    def find_corners(self): #Find 4 tiles which only have 2 edgeIDs found on other tiles
        self.corners=[] #List of corners
        ret=1 #Multiply corner IDs
        for s_k, s_v in self.tiles.items():
            neighbours=0
            for o_k, o_v in self.tiles.items():
                if s_k != o_k and s_v.shared_edge(o_v) is not None:
                    neighbours+=1
                    self.inner_edgeIDs.add(s_v.shared_edge(o_v))
            if neighbours==2:
                self.corners.append(s_v.tileID)
                ret*=s_v.tileID
        return(ret)

    def find_neighbour(self,tileID,side=3): #Find neighbour to tile on specified side
        edgeID=abs(self.tiles[tileID].edgeIDs_ordered[side])
        for s_k, s_v in self.tiles.items():
            if s_k!=tileID and edgeID in s_v.edgeIDs:
                return(s_v)

    def arrange_tiles(self):
        self.find_corners()
        self.tilegrid={}
        row_start=self.tiles[self.corners[0]] #Start with one of the corners
        #Rotate until bottom and left edges are inner edges
        while abs(row_start.edgeIDs_ordered[0]) in self.inner_edgeIDs or abs(row_start.edgeIDs_ordered[1]) in self.inner_edgeIDs:
            row_start.rotate()
        self.tilegrid[complex(0,0)]=row_start.tileID

        #Fill row
        current=row_start
        i=1
        j=0
        while j<self.dim:
            while i<self.dim:
                next=self.find_neighbour(current.tileID) #Find tileID of tile to the right

                self.tilegrid[complex(i,j)]=next.tileID #Add new tile to coordinate grid
                next.orient_to_match(current.edgeIDs_ordered[3]) #Rotate/reflect new tile to correct orientation
                current=next
                i+=1
            #Start new row
            j+=1
            i=0
            if j==self.dim: #End at the end of final row
                break
            next=self.find_neighbour(row_start.tileID,side=2) #Find tileID of new row start based on bottom edge of tile above
            self.tilegrid[complex(i,j)]=next.tileID #Add new tile to coordinate grid
            next.orient_to_match(row_start.edgeIDs_ordered[2],side=0) #Rotate/reflect new tile to correct orientation
            row_start=next
            current=next
            i+=1

    def create_image(self): #Combine tiles into one full image
        self.arrange_tiles()
        image_pixels={} #Pixel coordinates for full image
        for k_t, v_t in self.tilegrid.items(): #k_t=position of tile, v_t=tileID
            tile=self.tiles[v_t]
            for p_c, p_v in tile.pixels.items(): #p_c=coordinate of pixel within tile, p_v =#/.
                if 0<p_c.real<(tile.dim-1) and 0<p_c.imag<(tile.dim-1): #Remove outer edge of tile
                    coord=(tile.dim-2)*k_t+p_c-complex(1,1) #Position in full image = tile position * size of tile (after removing edges) + pixel position within tile - (1,1) (to shift origin to (0,0) after edge removal)
                    image_pixels[coord]=p_v
        self.image=Image(image_pixels)

    def count_monsters(self): #Count sea monsters in current image orientation
        count=0
        for j in range(self.image.dim-self.mon_height):
            for i in range(self.image.dim-self.mon_length):
                pos=complex(i,j)
                found=True
                for h in self.monster:
                    if self.image.pixels[pos+h] != '#':
                        found=False
                        break
                if found:
                    count+=1
                    for h in self.monster: #Add monster to map
                        self.image.pixels[pos+h]='O'

        return(count)

    def find_roughness(self): #Find sea monsters and count water roughness
        self.create_image()
        #Check 4 rotations, reflect, then check other 4 rotations
        for x in range(4):
            n=self.count_monsters()
            if n>0:
                print(self.image)
                return(self.image.hash_size - n*self.mon_size)
            if x<3:
                self.image.rotate(IDs=False)
        self.image.reflect(IDs=False)
        for x in range(4):
            n=self.count_monsters()
            if n>0:
                print(self.image)
                return(self.image.hash_size - n*self.mon_size)
            if x<3:
                self.image.rotate(IDs=False)
        return('No monsters found')        

system=System(input)
print(system.find_corners())
print(system.find_roughness())