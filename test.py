from json import dumps as pp
import random
from tabulate import tabulate
from PIL import Image, ImageDraw

class WaveFunctionCollapse:
    def __init__(self, image):
        self.image = image
        self.create_tile_data()
        for _ in range(1):
            self.create_grid()
            self.create_img(self.grid)

    def create_tile_data(self):
        self.tiles = {key: {"n": set(), "s": set(), "e": set(), "w": set()} for key in set(self.image) - {'\n'}}
        self.update_tiles(self.image)

    def update_tiles(self, image):
        temp_img = image.split("\n")
        length, breadth = len(temp_img[0]), len(temp_img)

        for j in range(breadth):
            for i in range(length):
                key = temp_img[j][i]
                for dir, dx, dy in (("n", 0, -1), ("s", 0, 1), ("e", 1, 0), ("w", -1, 0)):
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < length and 0 <= ny < breadth:
                        new_tile = temp_img[ny][nx]
                        if new_tile not in self.tiles[key][dir]:
                            self.tiles[key][dir].add(new_tile)

    def create_grid(self, length=50, breadth=50):
        self.length, self.breadth = length, breadth
        items = tuple(self.tiles.keys())
        self.grid = [[items for _ in range(length)] for _ in range(breadth)]
        self.copy = [[items for _ in range(length)] for _ in range(breadth)]

        tile = self.find_tile_collapse()

        while tile:
            fail = self.collapse_tile(tile)
            if fail:
                self.grid = self.update_grid()
            tile = self.find_tile_collapse()

        print(tabulate(self.grid, tablefmt='grid'), "\n\n")

    def find_entropy(self, x, y, items):
        if not isinstance(items, (list, tuple,set)):
            return float('inf'), items

        new_items = set(items)
        for state in items:
            for r_dir, dx, dy in (("s", 0, -1), ("n", 0, 1), ("w", 1, 0), ("e", -1, 0)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.length and 0 <= ny < self.breadth:
                    if len(self.grid[ny][nx]) == 1 and state not in self.tiles[state][r_dir]:
                        new_items.remove(state)
                        break

        return len(new_items), new_items

    def find_tile_collapse(self):
        self.et = [[None for _ in range(self.length)] for _ in range(self.breadth)]
        for j in range(self.breadth):
            for i in range(self.length):
                self.et[j][i] = self.find_entropy(i, j, self.grid[j][i])[0]

        low = min(min(row) for row in self.et)
        if low == float('inf'):
            return None

        tiles = [(i, j) for j, row in enumerate(self.et) for i, val in enumerate(row) if val == low]
        return random.choice(tiles) if tiles else None

    def update_grid(self):
        self.et = [[None for _ in range(self.length)] for _ in range(self.breadth)]
        for j in range(self.breadth):
            for i in range(self.length):
                self.et[j][i] = self.find_entropy(i, j, self.grid[j][i])[1]

        return self.et

    def collapse_tile(self, tile):
        x, y = tile
        items = self.grid[y][x]

        if not items:
            self.create_img(self.grid)
            self.grid = self.copy
            self.create_img(self.grid)
            print(self.grid)
            return False

        if len(items) > 1:
            self.copy = [row.copy() for row in self.grid]

        new_tile = random.choice(list(items))
        self.grid[y][x] = new_tile
        return True

    def create_img(self, grid):
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


image = """mlsslm
mlslmm
lssslm
mlsllm
mmlmmm"""
wfc = WaveFunctionCollapse(image)
