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


class WaveFunctionCollaspe:
    def __init__(self, tile_grid, tile_to_img, tile_size):

        self.tile_grid = tile_grid
        self.tile_name_to_image = tile_to_img
        self.tile_size = tile_size
        self.setup()

    def setup(self,):
        self.tiles = {key: {"n": set(), "s": set(), "e": set(), "w": set()}
                      for key in self.tile_name_to_image.keys()}
        self.update_tiledate(self.tile_grid)

    def generate(self, length=5, breadth=5, rad=True):

        self.repeat_count = 0
        self.length = length
        self.breadth = breadth
        self.randomfunc = self.random_entropy if rad else self.psudorandom_entropy
        self.creategrid()
        self.t2percent = 1 or int(0.01 * self.length * self.breadth)
        self.whensave = self.t2percent
        self.iter = 0
        self.last = 0

        tile = self.find_tile_collapse()

        while tile:
            if self.collapse_tile(tile[0], tile[1]):
                self.update_grid(tile)

            tile = self.find_tile_collapse()

            if self.repeat_count != self.last:
                print(self.repeat_count)
                self.last = self.repeat_count
                print(tabulate(self.entropy))
                self.show()
                self.create_img(self.grid)
                if self.iter > 2:
                    quit()
            self.iter += 1

            # self.show()
            # if self.iter % (0.2 * self.breadth * self.length) == 0:
            #     pass
            #     self.create_img(self.grid)

        self.create_img(self.grid)

    def update_tiledate(self, image):
        tempimg = image
        img_len, img_bre = len(tempimg[0]), len(tempimg)

        for j in range(img_bre):
            for i in range(img_len):
                key = tempimg[j][i]
                for dir, dx, dy in (("n", 0, -1), ("s", 0, 1), ("e", 1, 0), ("w", -1, 0)):
                    if 0 <= (i + dx) < img_len and 0 <= (j + dy) < img_bre:
                        newtile = tempimg[j + dy][i + dx]
                        self.tiles[key][dir].add(newtile)

    def creategrid(self):
        items = list(self.tiles.keys())
        self.grid = [[items for _ in range(self.length)]
                     for __ in range(self.breadth)]
        self.copy = [row.copy() for row in self.grid]
        self.entropy = {len(items): set(
            [(i, j) for i in range(self.length) for j in range(self.breadth)])}
        self.entropy_copy = {len(items): set(
            [(i, j) for i in range(self.length) for j in range(self.breadth)])}
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

    def psudorandom_entropy(self, min_entropy):
        a = self.entropy[min_entropy].pop()
        self.entropy[min_entropy].add(a)
        return a

    def random_entropy(self, min_entropy):
        return random.choice(list(self.entropy[min_entropy]))

    def update_grid(self, starttile):
        stack = [starttile]
        while stack != []:
            x, y = stack.pop()
            myitems = self.grid[y][x]
            if isinstance(myitems, str):
                myitems = [myitems]

            for rdir, nx, ny in (("n", x, y - 1), ("s", x, y + 1), ("e", x + 1, y), ("w", x - 1, y)):
                if (0 <= nx < self.length) and (0 <= ny < self.breadth) and not ((nx, ny) in self.reduced):
                    sidetile = self.grid[ny][nx]
                    if self.tile_reduced(nx, ny, sidetile, rdir, myitems):
                        stack.append((nx, ny))

    def tile_reduced(self, x, y, mytile, dirs, constraint):
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
            self.entropy[new_ent].add((x, y))
        else:
            self.entropy[new_ent] = {(x, y)}

        # self.entropy[len(mytile)] = [i for i in self.entropy[len(mytile)] if i != (x,y)]
        self.entropy[len(mytile)].remove((x, y))

        self.chk(len(mytile))
        self.grid[y][x] = newmytile
        return True

    def collapse_tile(self, x, y):

        items = self.grid[y][x]

        if len(items) == 0:
            self.grid = self.copy
            self.entropy = self.entropy_copy
            self.repeat_count += 1
            return False

        elif len(items) > 1 and self.whensave > self.iter:
            self.copy = [row.copy() for row in self.grid]
            self.entropy_copy = {
                key: self.entropy[key].copy() for key in self.entropy.keys()}
            self.whensave += self.t2percent

        self.grid[y][x] = random.choice(items)
        self.entropy[len(items)].remove((x, y))
        self.chk(len(items))
        self.reduced.add((x, y))
        return True

    def show(self, *args):
        print(tabulate(self.grid, tablefmt='grid'))
        print(*args, "\n")

    def create_img(self, grid):
        img_width = self.length * self.tile_size
        img_height = self.breadth * self.tile_size
        image = Image.new("RGB", (img_width, img_height), "white")

        for i, row in enumerate(grid):
            for j, tile in enumerate(row):
                try:
                    image.paste(
                    self.tile_name_to_image[tile], (j * self.tile_size, i * self.tile_size))
                except:
                    pass
        image.show(title="FINAL")
        return image

    def chk(self, key):
        if self.entropy[key] == set():
            del self.entropy[key]


class ImageTile:
    def __init__(self, path, tile_size):
        self.tile_size = tile_size
        self.image = Image.open(path)

    def cut(self):

        tiles = {}
        for j in range(self.tile_size, self.image.size[1] + self.tile_size, self.tile_size):
            for i in range(self.tile_size, self.image.size[0] + self.tile_size, self.tile_size):
                tiles[(i // self.tile_size - 1, j // self.tile_size - 1)
                      ] = self.image.crop((i - self.tile_size, j - self.tile_size, i, j))

        self.grid_length = self.image.size[0]//self.tile_size
        self.grid_breadth = self.image.size[1]//self.tile_size

        # create Unique tiles
        ids = "tile"
        count = 1
        self.unique_tiles = {}
        for i in tiles.values():
            if i not in self.unique_tiles.values():
                self.unique_tiles[ids + str(count)] = i
                count += 1
        print("done")
      

        # create tile grid

        key = list(self.unique_tiles.keys())
        val = list(self.unique_tiles.values())

        self.tile_grid = [[key[val.index(tiles[(x, y)])] for x in range(self.grid_length)] for y in range(self.grid_breadth)]

        return self.tile_grid, self.unique_tiles, self.tile_size

    def check(self):
        # recontruct image
        print("Start")
        img_width, img_height = self.image.size

        image = Image.new("RGB", (img_width, img_height), "white")

        for i, row in enumerate(self.tile_grid):
            for j, cell in enumerate(row):
                image.paste(self.unique_tiles[cell], (j * self.tile_size, i * self.tile_size))
        image.show(title="Recontruct")

        # display all tiles
        tile_set = self.unique_tiles.values()
        space_between_tiles = 4
        max_rows = None

        max_width = max(tile.width for tile in tile_set)
        max_height = max(tile.height for tile in tile_set)
        
        max_rows = max_rows or int(len(tile_set) ** 0.5)
        max_columns = len(tile_set) // max_rows + 1

        total_width = max_columns * (max_width + space_between_tiles) - space_between_tiles
        total_height = ((len(tile_set) - 1) // max_columns + 1) * (max_height + space_between_tiles) - space_between_tiles

        tile_img = Image.new("RGBA", (total_width, total_height), (0,0,0,0))

        current_x, current_y = 0, 0
        for tile in tile_set:
            tile_img.paste(tile, (current_x, current_y))

            current_x += max_width + space_between_tiles
            if current_x + max_width > total_width:
                current_x = 0
                current_y += max_height + space_between_tiles
        
        tile_img.show(title="tile grid")


image = ImageTile("Village.png", 2)

tile_grid, tile_to_img, tile_size = image.cut()

image.check()

# quit()

wfc = WaveFunctionCollaspe(tile_grid,tile_to_img,tile_size)

for i in range(1):
    wfc.generate(50,50,False)
