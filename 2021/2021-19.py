#Advent of Code 2021 Day 19
import re
from functools import total_ordering
from collections import defaultdict
f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-19.txt')
contents = f.read()
inp = contents.splitlines()

@total_ordering
class Coord(): #Coordinates in 3D space
    def __init__(self,x,y,z) -> None:
        self.x=int(x)
        self.y=int(y)
        self.z=int(z)
        
    def __repr__(self) -> str:
        return(f'({self.x}, {self.y}, {self.z})')

    def __str__(self) -> str:
        return(self.__repr__())

    def __eq__(self,other):
        return(self.x==other.x and self.y==other.y and self.z==other.z)

    def __hash__(self) -> int:
        return(hash((self.x,self.y,self.z)))

 
    def __lt__(self,other):
        if self.x!=other.x:
            return(self.x<other.x)
        elif self.y!=other.y:
            return(self.y<other.y)
        else:
            return(self.z<other.z)

    def rotate(self,n): #Return rotated coordinate, rotated by nth possible rotation
        #24 possible rotations
        rotation=((self.x, self.y, self.z),(self.x, -self.z, self.y),(self.x, -self.y, -self.z),(self.x, self.z, -self.y),(-self.y, self.x, self.z),(self.z, self.x, self.y),(self.y, self.x, -self.z),(-self.z, self.x, -self.y),(-self.x, -self.y, self.z),(-self.x, -self.z, -self.y),(-self.x, self.y, -self.z),(-self.x, self.z, self.y),(self.y, -self.x, self.z),(self.z, -self.x, -self.y),(-self.y, -self.x, -self.z),(-self.z, -self.x, self.y),(-self.z, self.y, self.x),(self.y, self.z, self.x),(self.z, -self.y, self.x),(-self.y, -self.z, self.x),(-self.z, -self.y, -self.x),(-self.y, self.z, -self.x),(self.z, self.y, -self.x),(self.y, -self.z, -self.x))[n]
        return(Coord(rotation[0],rotation[1],rotation[2]))

    def man_dist(self,other): #Manhatten distance between two Coords
        return(abs(self.x-other.x)+abs(self.y-other.y)+abs(self.z-other.z))

    def diff(self,other): #Difference between two Coords
        return(Coord(self.x-other.x,self.y-other.y,self.z-other.z))

    def add(self,other): #Addd two Coords
        return(Coord(self.x+other.x,self.y+other.y,self.z+other.z))


class Scanner(): #Scanner with a list of beacon coordinates, relative to itself
    def __init__(self,id) -> None:
        self.id=id
        self.beacons=set() #Set of beacons

    def add_beacon(self,beacon:Coord):
        self.beacons.add(beacon)

    def man_dists(self): #Calculate all manhatten distances between the scanner's beacons
        self.dists=set()
        for x in self.beacons:
            for y in self.beacons:
                if x!=y:
                    self.dists.add(x.man_dist(y))

    def __repr__(self) -> str:
        return(f'Scanner {self.id}')

    def __str__(self) -> str:
        return(self.__repr__())

class Region():
    def __init__(self,inp) -> None:
        p1=re.compile('--- scanner (\d+) ---')
        p2=re.compile('(-?\d+),(-?\d+),(-?\d+)')
        self.scanners={} #Dict of scanners, indexed by scanner ID (starts full, scanners removed as they are incorporated)
        self.scan_pos={} #Dict of scanner positions, indexed by scanner ID (starts empty, scanners added as they are incorporated)
        self.dists={} #Dict of manhatten distances, indexed by scanner ID (starts empty, scanners added as they are incorporated)
        self.all_beacons=set() #Set of all beacons
        self.beacons={} #Dict of beacons, indexed by scanner ID (starts empty, beacons added as scanners are incorporated)
        #Create Scanner objects based on input data
        for x in inp:
            if p1.match(x):
                m=p1.match(x)
                id=int(m.group(1))
                self.scanners[id]=Scanner(id)
            elif p2.match(x):
                m=p2.match(x)
                self.scanners[id].add_beacon(Coord(m.group(1),m.group(2),m.group(3)))
        for s in self.scanners.values(): #Initialise manhatten distances
            s.man_dists()
        #Set first scanner as origin point
        s=self.scanners.pop(0)
        self.beacons[0]=s.beacons.copy()
        for b in s.beacons:
            self.all_beacons.add(b)
        self.scan_pos[0]=Coord(0,0,0)
        self.dists[0]=s.dists.copy()

    def count_beacons(self):
        print(self.all_beacons)
        return(len(self.all_beacons))

    def add_all_scanners(self): #Bring in scanners one at a time until they are all incorporated into region
        failed=False
        while len(self.scanners)>0 and not failed:
            failed=self.add_scanner()
        print(f'Complete region contains {self.count_beacons()} beacons')

    def add_scanner(self): #Bring in scanner with most matching manhatten distances
        #Find scanner that overlaps most with incorporated region
        mx_overlap=0
        new_id=None
        for id,scanner in self.scanners.items(): #Scanners yet to be added
            #print(scanner)
            for r_id, dists in self.dists.items(): #Scanners already added
                matches=len(dists & scanner.dists)
                #print(f'{r_id}: {matches} matches')
                if matches>mx_overlap:
                    mx_overlap=matches
                    new_id=id
                    rjoin_id=r_id
        new_scanner=self.scanners.pop(new_id) #Pop new scanner from list
        print(f'{new_scanner} to be added to region using Scanner {rjoin_id} ({mx_overlap} matching manhatten distances)')
        self.dists[new_id]=new_scanner.dists
        #Try different rotations of new scanner and compare distances between beacons to find 12 pairs with matching offsets
        loop=True
        for r in range(24): #Loop through all possible rotations to find one where beacon pairs are only a constant offset away from each other
            if not loop:
                break
            offsets=defaultdict(int)
            for a in new_scanner.beacons:
                if not loop:
                    break
                a_rot=a.rotate(r)
                for b in self.beacons[rjoin_id]:
                    if not loop:
                        break
                    o=a_rot.diff(b)
                    offsets[o]+=1
                    if offsets[o]==12:
                        rot_i=r
                        offset=o
                        print(f'Rotation {rot_i}, offset {offset}')                        
                        loop=False
        if loop:
            print('WARNING: No offset found')
            return(False)
        #Transform all of new scanner's beacons using calculated rotation and offset
        region.beacons[new_id]=set()
        overlaps=0
        for beacon in new_scanner.beacons:
            b_rot=beacon.rotate(rot_i)
            b_rel_region=b_rot.diff(offset)
            if b_rel_region in region.beacons[rjoin_id]:
                overlaps+=1
            region.all_beacons.add(b_rel_region)
            region.beacons[new_id].add(b_rel_region)
        self.scan_pos[new_id]=offset #Record new scanner's position

    def scanner_man_dists(self): #Calculate all manhatten distances between the region's scanners
        self.scan_dists=set()
        for x in self.scan_pos.values():
            for y in self.scan_pos.values():
                if x!=y:
                    self.scan_dists.add(x.man_dist(y))
        print(max(self.scan_dists))

region=Region(inp)
region.add_all_scanners()
region.scanner_man_dists()

