"""Interface Sprites Module"""

import pyglet, os

class Board(pyglet.sprite.Sprite):
    """Board Sprite Class"""

    def __init__(self, size=3, center_x=0, center_y=0, margin=10, tilesize=103, padding=2):
        """Initialize class
        
        Arguments:
            size {int} -- number of rows and columns (default: {3})
            center_x {int} -- center position in x axis (default: {0})
            center_y {int} -- center position in y axis (default: {0})
            margin {int} -- board margin (default: {10})
            tilesize {int} -- tile size (default: {103})
            padding {int} -- space between tiles (default: {2})
        """
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
        """Check if (x, y) coordinates collides with the object
        
        Arguments:
            x {int}
            y {int}

        Returns:
            mixed -- bool, tuple (r, c) if collided with a cell
        """
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
        """Add tile to board
        
        Arguments:
            name {str} -- tile image name
            row {int} -- row number
            col {int} -- column number
            alt {bool} -- use alternate image (default: {False})
        """
        cellx = (self.x) + (self.tilesize * col) + (self.margin * (col + 1))
        celly = (self.y + self.height) - ((self.tilesize + self.margin) * (row + 1))
        tile = Button(name, cellx, celly, alt)
        tile.scale = self.tilesize / 103
        self.tiles['{},{}'.format(row, col)] = tile

    def add_arrow(self, d, row, col):
        """Add arrows to board
        
        Arguments:
            d {str} -- arrow direction
            row {int} -- row number
            col {int} -- column number
        """
        celly = (self.y + self.height) - ((self.tilesize + self.margin) * (row + 1))
        arrow = Button('arrow_{}'.format(d))
        arrow.x = ((self.x) + ((self.tilesize + self.margin) * (col + 1)) - (self.tilesize / 2)) - (arrow.width / 2)
        arrow.y = (celly) + (self.tilesize / 2) - (arrow.height / 2)     
        self.arrows['{},{}'.format(row, col)] = arrow

    def clear_tiles(self):
        """Clear board tiles"""
        self.tiles = {}

    def clear_arrows(self):
        """Clear board arrows"""
        self.arrows = {}

class Button(pyglet.sprite.Sprite):
    """Button Sprite Class"""

    def __init__(self, name, x=0, y=0, alt=False):
        """Initialize class
        
        Arguments:
            name {str} -- button image name
            x {int} -- position x (default: {0})
            y {int} -- position y (default: {0})
            alt {bool} -- use alternate name (default: {False})
        """
        super().__init__(pyglet.image.load('images/{}.png'.format(name)), x=x, y=y)
        self.set_image(name, alt, None)
        
    def set_state(self, value:int):
        """Set button state
        
        Arguments:
            value {int}
        """
        self.set_image(self.name, self.alt, value)
        
    def set_image(self, name, alt=False, state=None):
        """Set button image
        
        Arguments:
            name {str} -- button image name
            alt {bool} -- use alternate image (default: {False})
            state {int} -- button state (default: {None})
        """
        self.name, self.state, self.alt = name, state, alt
        path = 'images/{}.png'.format('_'.join([str(x) for x in [self.name, 'alt' if self.alt else None, self.state] if x is not None]))
        if os.path.exists(path):
            self.image = pyglet.image.load(path)

    @property
    def disabled(self):
        """Get disabled property

        Returns:
            bool
        """
        return self.state == 0

    @disabled.setter
    def disabled(self, value:bool):
        """Set disabled property

        Arguments:
            value {bool}
        """
        self.set_state(0 if value is True else None)

    @property
    def focused(self):
        """Get focused property

        Returns:
            bool
        """
        return self.state == 1

    @focused.setter
    def focused(self, value:bool):
        """Set focused property

        Arguments:
            value {bool}
        """
        self.set_state(1 if value is True else None)

    def collide(self, x, y):
        """Check if (x, y) coordinates collides with the object
        
        Arguments:
            x {int}
            y {int}

        Returns:
            bool
        """
        if x in range(int(self.x), int(self.x + self.width)) and y in range(int(self.y), int(self.y + self.height)):
            return True
        return False