from collections import Counter
import re

f = open('C:/Users/Simon/OneDrive/Home Stuff/Python/Advent of Code/2021/2021-05.txt')
contents = f.read()
inp = contents.splitlines()

def count_crossovers(inp,diag=False):
    c=Counter()
    p=re.compile('^(\d+),(\d+) -> (\d+),(\d+)$') #regex for lines
    for line in inp:
        m=re.match(p,line)
        x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
        y_min=min(y1,y2)
        y_max=max(y1,y2)
        x_min=min(x1,x2)
        x_max=max(x1,x2)
        #print(line)
        if x1==x2: #Vertical line
            for y in range(y_min,y_max+1):
                c.update([complex(x1,y)])
                #print(complex(x1,y))
        elif y1==y2: #Horizontal line
            for x in range(x_min,x_max+1):
                c.update([complex(x,y1)])
                #print(complex(x,y1))
        elif diag: #Consider diagonal lines
            slope=int((y2-y1)/(x2-x1))
            if slope==1: #Positive slope
                for i in range(y_max-y_min+1):
                    c.update([complex(x_min+i,y_min+i)])
                    #print(complex(x_min+i,y_min+i))
            elif slope==-1: #Negative slope
                for i in range(y_max-y_min+1):
                    c.update([complex(x_max-i,y_min+i)])
                    #print(complex(x_max-i,y_min+i))
            else:
                print('Unexpected slope of {}'.format(slope))

    #Draw map
    minX=int(min(c.keys(),key=lambda x:x.real).real)
    maxX=int(max(c.keys(),key=lambda x:x.real).real)
    minY=int(min(c.keys(),key=lambda x:x.imag).imag)
    maxY=int(max(c.keys(),key=lambda x:x.imag).imag)
    ret=''
    for j in range(minY,maxY+1):
        for i in range(minX,maxX+1):
            if complex(i,j) in c.keys():
                ret+=str(c[complex(i,j)])
            else:
                ret+='.'
        ret+='\n'
    #print(ret)


    crossovers={k:v for k, v in c.items() if v>1} #Points visited more than once
    #print(c)
    return(len(crossovers))

print(count_crossovers(inp))
print(count_crossovers(inp,diag=True)) #19086 too low