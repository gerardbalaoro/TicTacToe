import pyglet
from pyglet.gl import *


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.set_minimum_size(400, 300)
        #self.set_maximum_size(1600, 1200)

        self.main_menu()

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

    def main_menu(self):
        self.background = pyglet.image.load('resources/Main_Menu_final.jpg')

    def rules(self, mode):
        if mode == '3x3':
            self.background = pyglet.image.load('resources/Rules_of_3x3_final.jpg')
        elif mode == 'Flip':
            self.background = pyglet.image.load('resources/Rules_of_Flip_final.jpg')
        elif mode == 'Ulti':
            self.background = pyglet.image.load('resources/rules_of_ultimate.jpg')

    def board_reg(self):
        self.background = pyglet.image.load('resources/3X3_game_final.jpg')

    def board_flip(self):
        self.background = pyglet.image.load('resources/Flip_tac_toe_game.jpg')

    def board_ulti(self):
        self.background = pyglet.image.load('resources/ultimate_game.jpg')
        

def app():
    pyglet.app.run()

