import pyglet
from pyglet.gl import *

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background = pyglet.image.load('resources/main_menu.jpg')
        self.currentscreen = 'Main Menu'
        self.main()

    def on_draw(self):
        self.clear()

        bg = pyglet.sprite.Sprite(self.background, x=0, y=0)
        bg.scale = 0.5
        bg.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.currentscreen == 'Main Menu':
            if x in range(200, 630) and y in range(315, 350):
                self.rules('3x3')
            elif x in range(180, 630) and y in range(230, 265):
                self.rules('Flip')
            elif x in range(100, 700) and y in range(150, 190):
                self.rules('Ulti')
            elif ((x in range(100, 220) and y in range(45, 70)) or
                  (x in range(80, 235) and y in range(70, 105))):
                self.load()

        elif self.currentscreen[0] == 'Rules':
            if (((x-380)**2)/10) + (((y-90)**2)/5) <= 25**2:
                self.board(self.currentscreen[1])
            elif ((x in range(560, 760) and y in range(480, 500)) or
                  (x in range(610, 720) and y in range(500, 545))):
                self.main()

        elif self.currentscreen[0] == 'Board':
            """Board Clicking"""
            if ((x in range(45, 243) and y in range(48, 62)) or
                    (x in range(80, 180) and y in range(62, 110))):
                self.save(self.currentscreen)
                

    def main(self):
        self.background = pyglet.image.load('resources/main_menu.jpg')
        self.currentscreen = 'Main Menu'

    def save(self, game):
        """Saving stuff"""
        self.main()

    def load(self):
        """Loading stuff"""
        pass

    def rules(self, mode):
        self.currentscreen = ('Rules', mode)

        if mode == '3x3':
            self.background = pyglet.image.load('resources/rules_3x3.jpg')
        elif mode == 'Flip':
            self.background = pyglet.image.load('resources/rules_flip.jpg')
        elif mode == 'Ulti':
            self.background = pyglet.image.load('resources/rules_ultimate.jpg')

    def board(self, mode):
        self.currentscreen = ('Board', mode)

        if mode == '3x3':
            self.background = pyglet.image.load('resources/3x3_game.jpg')
        elif mode == 'Flip':
            self.background = pyglet.image.load('resources/flip_game.jpg')
        elif mode == 'Ulti':
            self.background = pyglet.image.load('resources/ultimate_game.jpg')

def app():
    pyglet.app.run()

