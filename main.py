from json import dumps as pp
import random
from tabulate import tabulate
from PIL import Image, ImageDraw

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
        for i in range(1):
   
            self.generate(500,500)

    def setup(self):
        self.create_tiledata()
        self.update_tiledate(self.image)

    def generate(self,length = 5,breadth = 5):
        self.repeat_count = 0
        self.length = length
        self.breadth = breadth
        self.creategrid()

        tile  = self.find_tile_collapse()
        
        while tile:
            notfail = self.collapse_tile(tile[0],tile[1])
            if notfail == True:
                self.update_grid(tile)
                
            tile = self.find_tile_collapse()
         

        
        self.show("FINAL",self.repeat_count)
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
        self.entropy = [[None for _ in range(self.length)] for j in range(self.breadth)]
            
    def find_tile_collapse(self):
        low = float('inf')
        tiles = []
        for j in range(self.breadth):
            for i in range(self.length):
                if not isinstance(self.grid[j][i],str):
                    size = len(self.grid[j][i])
                    if size == low:
                        tiles.append((i,j))
                    elif size < low:
                        low = size
                        tiles.clear()
                        tiles.append((i,j))
        if low == float('inf'):
            return None
        else:
            return random.choice(tiles)
    
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

        self.grid[y][x] = newmytile
        return reduced
      
    def collapse_tile(self,x,y):
        items = self.grid[y][x]

        if len(items) == 0:
            self.grid = self.copy
            self.repeat_count += 1
            return False

        elif len(items) > 1:
            self.copy = [row.copy() for row in self.grid]

        self.grid[y][x] = random.choice(items)
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



wfc = WaveFunctionCollaspe(image)
