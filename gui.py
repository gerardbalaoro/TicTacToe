import pyglet
from pyglet.gl import *


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.set_minimum_size(400, 300)
        # self.set_maximum_size(1600, 1200)

        self.background = pyglet.image.load('resources/Main_Menu_final.jpg')
        self.currentscreen = 'Main Menu'
        self.main()

    """
    #if window is resizable
    def on_resize(self, width, height):
        self.set_size(width, int(width*3/4))

        viewport = self.get_viewport_size()
        gl.glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    """

    def on_draw(self):
        self.clear()

        bg = pyglet.sprite.Sprite(self.background, x=0, y=0)
        bg.scale = self.width / 1600
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
                print('PLAY')
            elif ((x in range(560, 760) and y in range(480, 500)) or
                  (x in range(610, 720) and y in range(500, 545))):
                self.main()
        elif self.currentscreen[0] == 'Board':
            pass

    def main(self):
        self.background = pyglet.image.load('resources/Main_Menu_final.jpg')
        self.currentscreen = 'Main Menu'

    def load(self):
        pass

    def rules(self, mode):
        self.currentscreen = ('Rules', mode)
        if mode == '3x3':
            self.background = pyglet.image.load('resources/Rules_of_3x3_final.jpg')
        elif mode == 'Flip':
            self.background = pyglet.image.load('resources/Rules_of_Flip_final.jpg')
        elif mode == 'Ulti':
            self.background = pyglet.image.load('resources/rules_of_ultimate.jpg')

    def board(self, mode):
        if mode == '3x3':
            self.background = pyglet.image.load('resources/3X3_game_final.jpg')
        elif mode == 'Flip':
            self.background = pyglet.image.load('resources/Flip_tac_toe_game.jpg')
        elif mode == 'Ulti':
            self.background = pyglet.image.load('resources/ultimate_game.jpg')

def app():
    pyglet.app.run()
