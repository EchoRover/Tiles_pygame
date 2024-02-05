from json import dumps as pp
import random
from tabulate import tabulate
from PIL import Image, ImageDraw
import cProfile
import heapq

image = """mlsslm
mlslmm
lssslm
mlsllm
mmlmmm"""

image2 = """lllllmsssb
lllmsbsylb
lrsbssylrs
rsssslrsbl
sblbllllms
ssslblmsbs
lymssslrll
lsssslyssy
sllllllrsr
lbmsyrblbl"""

image1 = """lllllmsssb
lllusbsylb
lrsbsmylrs
rssuslsrbl
sblbllllms
ssslblmsbs
lymssslrll
lsssslyssy
sllllllrsr
lbsmyrblbl"""


class WaveFunctionCollaspe:
    def __init__(self,image):
    

        self.image = image
        self.setup()
 

    def setup(self):
        self.create_tiledata()
        self.update_tiledate(self.image)

    def generate(self,length = 5,breadth = 5,random = True):
        self.repeat_count = 0
        self.length = length
        self.breadth = breadth
        self.randomfunc = self.random_entropy if random else self.psudorandom_entropy
        self.creategrid()

        tile  = self.find_tile_collapse()
        self.iter = 0
        
        while tile:
            notfail = self.collapse_tile(tile[0],tile[1])

            if notfail == True:
                self.update_grid(tile)
            else:
                print("fali")
                
            tile = self.find_tile_collapse()

            if self.repeat_count > 10:
                print(self.repeat_count)
            self.iter += 1

       


            # self.show()
            # if self.iter % (0.2 * self.breadth * self.length) == 0:
            #     pass
            #     self.create_img(self.grid)
        self.create_img(self.grid)
   
    def create_tiledata(self):
        self.tiles = {key:{"n":set(),"s":set(),"e":set(),"w":set()} for key in set(list(self.image))}
        del self.tiles["\n"]
 
    def update_tiledate(self,image):
        tempimg = image.split("\n")
        img_len,img_bre = len(tempimg[0]),len(tempimg)

        for j in range(img_bre):
            for i in range(img_len):
                key = tempimg[j][i]
                for dir,dx,dy in  (("n",0,-1),("s",0,1),("e",1,0),("w",-1,0)):
                    if 0 <= (i + dx) < img_len and 0 <= (j + dy) < img_bre:
                        newtile = tempimg[j + dy][i + dx]
                        self.tiles[key][dir].add(newtile)
    
    def creategrid(self):
        items = list(self.tiles.keys())
        self.grid = [[items for _ in range(self.length)] for __ in range(self.breadth)]
        self.copy = [row.copy() for row in self.grid]
        self.entropy = {len(items):set([(i,j) for i in range(self.length) for j in range(self.breadth)])}
        self.reduced = set()
        
    def find_tile_collapse(self):

        try:
            min_entropy = min(self.entropy.keys())
        except:
            return None
        if self.entropy[min_entropy] == set():
            return None
        else:
            return self.randomfunc(min_entropy)
    def psudorandom_entropy(self,min_entropy):
        a = self.entropy[min_entropy].pop()
        self.entropy[min_entropy].add(a)
        return a
    def random_entropy(self,min_entropy):
        return random.choice(list(self.entropy[min_entropy]))
        
    def update_grid(self,starttile):
        stack = [starttile]
        while stack != []:
            x,y = stack.pop()
            myitems = self.grid[y][x] 
            if isinstance(myitems,str):
                myitems = [myitems]
            
            for rdir,nx,ny in  (("n",x,y - 1),("s",x,y + 1),("e",x + 1,y),("w",x - 1,y)):
                if (0 <= nx < self.length) and (0 <= ny < self.breadth) and not((nx,ny) in self.reduced):
                    sidetile = self.grid[ny][nx]
                    if self.tile_reduced(nx,ny,sidetile,rdir,myitems):
                        stack.append((nx,ny))

    def tile_reduced(self,x,y,mytile,dirs,constraint):
        newmytile = mytile.copy()
        reduced = False
        for tile in mytile:
            for other in constraint:
                if tile in self.tiles[other][dirs]:
                    break
            else:
                newmytile.remove(tile)
                reduced = True
        if not reduced:
            return False

        new_ent = len(newmytile)

        if new_ent in self.entropy:
            self.entropy[new_ent].add((x,y))
        else:
            self.entropy[new_ent] = {(x,y)}     
        
        # self.entropy[len(mytile)] = [i for i in self.entropy[len(mytile)] if i != (x,y)]
        self.entropy[len(mytile)].remove((x,y))

        self.chk(len(mytile))
        self.grid[y][x] = newmytile
        return True
      
    def collapse_tile(self,x,y):
  
        items = self.grid[y][x]

        if len(items) == 0:
            self.grid = self.copy
            self.repeat_count += 1
            return False

        # elif len(items) > 1:
        #     self.copy = [row.copy() for row in self.grid]

        self.grid[y][x] = random.choice(items)

        self.entropy[len(items)].remove((x,y))
        self.chk(len(items))
        self.reduced.add((x,y))

        
        return True
    
    def show(self,*args):
        print(tabulate(self.grid,tablefmt = 'grid'))
        print(*args,"\n")

    def create_img(self,grid):
        cell_size = 15  # Adjust as needed
        img_width = len(grid[0]) * cell_size
        img_height = len(grid) * cell_size

        image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(image)

        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                color = (255, 255, 255)  # Default color (white)

                if cell == 'm':
                    color = (0, 238, 0)  # Gray for mountains
                elif cell == 'l':
                    color = (114, 79, 43)  # green for land
                elif cell == 'g':
                    color = (144, 238, 144)  # light green for grassland
                elif cell == 's':
                    color = (0, 0, 128)  # dark blue for standard sea
                elif cell == 'b':
                    color = (255, 228, 196)  # beige for beach
                elif cell == 'e':
                    color = (173, 216, 230)  # light blue for light ocean
                elif cell == 'd':
                    color = (0, 0, 139)  # dark blue for deep ocean
                elif cell == 'a':
                    color = (154, 205, 50)  # olive green for light land
                elif cell == 'y':
                    color = (210, 180, 140)  # tan for sandy land
                elif cell == 'r':
                    color = (169, 169, 169)  # dark gray for rocky land



                draw.rectangle([j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size], fill=color)

        image.show()

    def chk(self,key):
        if self.entropy[key] == set():
            del self.entropy[key]

class ImageTile:
    def __init__(self,path,size):
        self.path = path
        self.size = size
        self.image = Image.open(self.path)
        return self.cut()

    def cut(self):
        s = self.size
        parts = {}
        # grid = [[" " for i in range(self.image.size[0] + self.size)] for j in range(self.image.size[1] + self.size)]
        for j in range(self.size,self.image.size[1] + self.size,self.size):
            for i in range(self.size,self.image.size[0] + self.size,self.size):
                # grid[j][i] = "*"
                # print(i,j)
                parts[(i // s - 1,j // s - 1)] = self.image.crop((i - s,j - s,i,j))
        l = self.image.size[0]//self.size
        b = self.image.size[1]//self.size
        
   

        ids = "tile"
        count = 1
        unique = {}
        tiles = {}
        for i in parts.values():
            if i not in unique.values():
                unique[ids + str(count)] = i
                count += 1

        key = list(unique.keys())
        val = list(unique.values())

            
      
        self.imgg = [[key[val.index(parts[(x,y)])] for x in range(l)] for y in range(b)]
        for i in self.imgg:
            print(i)
        print(self.imgg)

        img_width,img_height = self.image.size

        image = Image.new("RGB", (img_width, img_height), "white")

        for i, row in enumerate(self.imgg):
            for j, cell in enumerate(row):
                image.paste(unique[cell],(j * self.size,i * self.size))
        # image.show()



        return self.imgg,unique



    
    

        
    
 


    




new_image = """lymaadggds
msrrsrsrll
arllllllla
gblblbsybr
ssyssssyss
ysyrrysyys
dyyayydyrs
mgyyymgyrs
lmgggmgmrl
sllsslllls"""

img,dicts = ImageTile("Lines.png",2)

wfc = WaveFunctionCollaspe(image)
# # wfc.create_img(new_image.split("\n"))
# wfc.generate(50,50)

# wfc.show("FINAL repeat =",wfc.repeat_count,"iter =",wfc.iter)
# wfc.create_img(wfc.grid)
