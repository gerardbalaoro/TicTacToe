import pyglet

class Board(pyglet.sprite.Sprite):
    def __init__(self, size=3, center_x=0, center_y=0):
        super().__init__(pyglet.image.load('objects/board_{}.png'.format(size)))
        self.x = center_x - (self.width / 2)
        self.y = center_y - (self.height / 2)

    def collide(self, x, y):
        if x in range(int(self.x), int(self.x + self.width)) and y in range(int(self.y), int(self.y + self.height)):
            return True
        return False

class Button(pyglet.sprite.Sprite):

    disabled = False
    inverted = False

    def __init__(self, name, x=0, y=0):
        super().__init__(pyglet.image.load('objects/{}.png'.format(name)), x=x, y=y)
        self.imagename = name

    def reset(self):
        path = 'objects/{}.png'.format(self.imagename)
        self.image = pyglet.image.load(path)
        return self

    def disable(self):
        path = 'objects/{}_0.png'.format(self.imagename)
        self.image = pyglet.image.load(path)
        return self

    def invert(self):
        path = 'objects/{}_2.png'.format(self.imagename)
        self.image = pyglet.image.load(path)
        return self

    def collide(self, x, y):
        if x in range(int(self.x), int(self.x + self.width)) and y in range(int(self.y), int(self.y + self.height)):
            return True
        return False

class Cross(Button):
    def __init__(self, x=0, y=0):
        super().__init__('cross', x=x, y=y)
        
class Circle(Button):
    def __init__(self, x=0, y=0):
        super().__init__('circle', x=x, y=y)