import pyglet
from pyglet.gl import *


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_minimum_size(400, 300)
        self.set_maximum_size(1600, 1200)

        bg_image = pyglet.image.load('resources/Main_Menu_final.jpg')
        self.bg = pyglet.sprite.Sprite(bg_image, x=0, y=0)

    def on_resize(self, width, height):
        self.set_size(width, int(width*3/4))

        viewport = self.get_viewport_size()
        gl.glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def on_draw(self):
        self.clear()

        self.bg.scale = self.width / 1600
        self.bg.draw()

    def main_menu(self):
        bg_image = pyglet.image.load('resources/Main_Menu_final.jpg')
        self.bg = pyglet.sprite.Sprite(bg_image, x=0, y=0)


def app():
    pyglet.app.run()

