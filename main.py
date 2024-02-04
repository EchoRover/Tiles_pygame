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

    def generate(self,length = 5,breadth = 5):
        self.repeat_count = 0
        self.length = length
        self.breadth = breadth
        self.creategrid()

        tile  = self.find_tile_collapse()
        self.iter = 0
        
        while tile:
            notfail = self.collapse_tile(tile[0],tile[1])

            if notfail == True:
                self.update_grid(tile)
                
            tile = self.find_tile_collapse()

            if self.repeat_count > 10:
                print(self.repeat_count)
            self.iter += 1

            # self.show()
            # if self.iter % (0.2 * self.breadth * self.length) == 0:
            #     pass
            #     self.create_img(self.grid)
            
         

        
        

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
        self.entropy = [[len(items) for _ in range(self.length)] for j in range(self.breadth)]
        self.entropy2 = {len(items):[(i,j) for i in range(self.length) for j in range(self.breadth)]}
        
    
    
    def find_tile_collapse(self):
        # print(self.entropy2,"\n\n")

        try:
            min_entropy = min(self.entropy2.keys())
        except:
            return None
        if self.entropy2[min_entropy] == []:
            return None
        else:
            return random.choice(self.entropy2[min_entropy])
        
        # min_entropy = float('inf')
        # min_indices = set()

        # for j in range(self.breadth):
        #     for i in range(self.length):
        #         current_entropy = self.entropy[j][i]

        #         if current_entropy == min_entropy:
        #             min_indices.add((i, j))
        #         elif current_entropy < min_entropy:
        #             min_entropy = current_entropy
        #             min_indices = {(i,j)}

        # if min_entropy == float('inf'):
        #     return None
        # else:
        #     return random.choice(list(min_indices))
    
    def update_grid(self,starttile):
        stack = [starttile]
        while stack != []:
            x,y = stack.pop()
            myitems = self.grid[y][x] 
            if isinstance(myitems,str):
                myitems = [myitems]
            
            for rdir,nx,ny in  (("n",x,y - 1),("s",x,y + 1),("e",x + 1,y),("w",x - 1,y)):
                if 0 <= nx < self.length and 0 <= ny < self.breadth and not isinstance(self.grid[ny][nx],str):
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

        new_ent = len(newmytile)
        if new_ent in self.entropy2:
            self.entropy2[new_ent].append((x,y))
        else:
            self.entropy2[new_ent] = [(x,y)] 
        self.entropy2[len(mytile)].remove((x,y))
        self.chk(len(mytile))


        self.entropy[y][x] = new_ent


        self.grid[y][x] = newmytile
        return reduced
      
    def collapse_tile(self,x,y):
        items = self.grid[y][x]

        if len(items) == 0:
            self.grid = self.copy
            self.repeat_count += 1
            return False

        # elif len(items) > 1:
        #     self.copy = [row.copy() for row in self.grid]

        self.grid[y][x] = random.choice(items)
        self.entropy[y][x] = float('inf')
        self.entropy2[len(items)].remove((x,y))
        self.chk(len(items))
        
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
                    color = (50, 168, 82)  # Gray for mountains
                elif cell == 'l':
                    color = (139, 69, 19)  # green for land
                elif cell == 's':
                    color = (0, 0, 128)  # Navy blue for sea


                draw.rectangle([j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size], fill=color)

        image.show()

    def chk(self,key):
        if self.entropy2[key] == []:
            del self.entropy2[key]



wfc = WaveFunctionCollaspe(image)
cProfile.run("wfc.generate(10,10)")

# wfc.show("FINAL repeat =",wfc.repeat_count,"iter =",wfc.iter)
wfc.create_img(wfc.grid)
