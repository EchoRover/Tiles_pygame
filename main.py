from json import dumps as pp
import random
from tabulate import tabulate
from PIL import Image, ImageDraw
image = """mlsslm
mlslmm
lssslm
mlsllm
mmlmmm"""


class WaveFunctionCollaspe:
    def __init__(self,image):
    

        self.image = (image)
        self.create_tiledata()
        for i in range(1):
            self.creategrid()
            create_img(self.grid)
    

    def create_tiledata(self):
        self.tiles = {key:{"n":[],"s":[],"e":[],"w":[]} for key in set(list(self.image))}
        del self.tiles["\n"]
        self.update_tiles(self.image)
        # print(pp(self.tiles,indent=2))
    
    def update_tiles(self,image):
        tempimg = image.split("\n")
        length = len(tempimg[0])
        breadth = len(tempimg)

        for j in range(breadth):
            for i in range(length):
                key = tempimg[j][i]
                for dir,dx,dy in  (("n",0,-1),("s",0,1),("e",1,0),("w",-1,0)):
                    if 0 <= (i + dx) < length and 0 <= (j + dy) < breadth:
                        newtile = tempimg[j + dy][i + dx]
                        if newtile not in self.tiles[key][dir]:
                            self.tiles[key][dir].append(newtile)
    

    def creategrid(self,length = 10,breadth = 10):
        self.length = length
        self.breadth = breadth
     
        
        items = tuple(self.tiles.keys())

        self.grid = [[items for _ in range(length)] for __ in range(breadth)]
        self.copy = [[items for _ in range(length)] for __ in range(breadth)]
      
    

    
        tile  = self.find_tile_collapse()

        while tile:
            # print(tabulate(self.grid,tablefmt = 'grid'),"\n\n")
            fail = self.collapse_tile(tile)
            if fail == True:
                self.grid = self.update_grid()
            tile = self.find_tile_collapse()
        
        print(tabulate(self.grid,tablefmt = 'grid'),"\n\n")
        
    
    def findenthorpy(self,x,y,items):
        if type(items) not in (list,tuple):
    
            return float('inf'),items
        newitems = list(items)
        for state in items:
            for rdir,dx,dy in  (("s",0,-1),("n",0,1),("w",1,0),("e",-1,0)):
                nx,ny = x + dx,y + dy
                if 0 <= nx < self.length and 0 <= ny < self.breadth:
                    if len(self.grid[ny][nx]) == 1:
                        sidetile = self.grid[ny][nx][0]
                        if sidetile in self.tiles[state][rdir]:
                            pass
                        else:
                            
                            newitems.remove(state)
                            break
        # if len(newitems) == 0:
        #     print(tabulate(self.grid,tablefmt = 'grid'),"\n\n")
            
        #     print("error")
        return len(newitems),newitems
    
    def find_tile_collapse(self):
        self.et = [[None for _ in range(self.length)] for j in range(self.breadth)]
        for j in range(self.breadth):
            for i in range(self.length):
                self.et[j][i] = self.findenthorpy(i,j,self.grid[j][i])[0]
        # print(tabulate(self.et,tablefmt="grid"))
        low = float('inf')
        for row in self.et:
            low = min(low,*row)
        if low == float('inf'):
            return None
        # print(low)
        
        tiles = []
        for j in range(self.breadth):
            for i in range(self.length):
                if self.et[j][i] == low:
                    tiles.append((i,j))
        
        
        return random.choice(tiles)
    
    def update_grid(self):
        self.et = [[None for _ in range(self.length)] for j in range(self.breadth)]
        for j in range(self.breadth):
            for i in range(self.length):
                self.et[j][i] = self.findenthorpy(i,j,self.grid[j][i])[1]
        
        return self.et
    
    
    def collapse_tile(self,tile):
        global GGGGG
        x,y = tile
        items = self.grid[y][x]
        if len(items) == 0:
            create_img(self.grid)
            self.grid = self.copy
            create_img(self.grid)
          
           
            print(self.grid,GGGGG)
            GGGGG += 1


            # print(tabulate(self.grid,tablefmt = 'grid'),"\n\n")

            return False
        elif len(items) > 1:
            self.copy = [row.copy() for row in self.grid]

        newtile = random.choice(items)
    
        self.grid[y][x] = newtile
        return True
    



GGGGG = 0

def create_img(grid):
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
                color = (139, 69, 19)  # Brown for land
            elif cell == 's':
                color = (0, 0, 128)  # Navy blue for sea

            draw.rectangle([j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size], fill=color)

    image.show()


    

        
                



    

wfc = WaveFunctionCollaspe(image)
# create_img(wfc.grid)