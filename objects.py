import pyglet, os

class Board(pyglet.sprite.Sprite):
    def __init__(self, size=3, center_x=0, center_y=0, margin=10, tilesize=103, padding=2):
        super().__init__(pyglet.image.load('images/board_{}.png'.format(size)))
        self.x = center_x - (self.width / 2)
        self.y = center_y - (self.height / 2)
        self.size = size
        self.tiles = {}
        self.arrows = {}
        self.margin = margin
        self.tilesize = tilesize if tilesize is not None else 103
        self.padding = padding

    def collide(self, x, y):
        if x in range(int(self.x), int(self.x + self.width)) and y in range(int(self.y), int(self.y + self.height)):
            row, col = None, None
            for i in range(self.size):
                cellx = int(self.x) + self.margin + ((self.tilesize + self.margin) * i)
                if x in range(cellx + (self.padding * i + 1), (cellx + self.tilesize) - (self.padding * i + 1)):
                    col = i
                    break
            for i in range(self.size):
                celly = int(self.y) + self.margin + ((self.tilesize + self.margin) * i)
                if y in range(celly + (self.padding * i + 1), (celly + self.tilesize) - (self.padding * i + 1)):
                    row = self.size - i - 1
                    break
            if row is not None and col is not None:
                return row, col
            return True
        return False

    def add_tile(self, name, row, col, alt=False):
        cellx = (self.x) + (self.tilesize * col) + (self.margin * (col + 1))
        celly = (self.y + self.height) - ((self.tilesize + self.margin) * (row + 1))
        tile = Button(name, cellx, celly, alt)
        tile.scale = self.tilesize / 103
        self.tiles['{},{}'.format(row, col)] = tile

    def add_arrow(self, d, row, col):
        celly = (self.y + self.height) - ((self.tilesize + self.margin) * (row + 1))
        arrow = Button('arrow_{}'.format(d))
        arrow.x = ((self.x) + ((self.tilesize + self.margin) * (col + 1)) - (self.tilesize / 2)) - (arrow.width / 2)
        arrow.y = (celly) + (self.tilesize / 2) - (arrow.height / 2)     
        self.arrows['{},{}'.format(row, col)] = arrow

    def clear_tiles(self):
        self.tiles = {}

    def clear_arrows(self):
        self.arrows = {}

class Button(pyglet.sprite.Sprite):

    def __init__(self, name, x=0, y=0, alt=False):
        super().__init__(pyglet.image.load('images/{}.png'.format(name)), x=x, y=y)
        self.set_image(name, alt, None)
        
    def set_state(self, value:int):
        self.set_image(self.name, self.alt, value)
        
    def set_image(self, name, alt=False, state=None):
        self.name, self.state, self.alt = name, state, alt
        path = 'images/{}.png'.format('_'.join([str(x) for x in [self.name, 'alt' if self.alt else None, self.state] if x is not None]))
        if os.path.exists(path):
            self.image = pyglet.image.load(path)

    @property
    def disabled(self):
        return self.state == 0

    @disabled.setter
    def disabled(self, value:bool):
        self.set_state(0 if value is True else None)

    @property
    def focused(self):
        return self.state == 1

    @focused.setter
    def focused(self, value:bool):
        self.set_state(1 if value is True else None)

    @property
    def inverted(self):
        return self.state == 2

    @inverted.setter
    def inverted(self, value:bool):
        self.set_state(2 if value is True else None)

    def collide(self, x, y):
        if x in range(int(self.x), int(self.x + self.width)) and y in range(int(self.y), int(self.y + self.height)):
            return True
        return False