import pyglet
from pyglet.gl import *
from objects import *
from wrapper import *

class Interface(pyglet.window.Window):
    def __init__(self, engine:Game):
        # Initialize Game Window
        super().__init__(width=800, height=600, caption='Tic Tac Toe Unlimited', resizable=False)
        
        # Game Image Assets
        self.images = {
            'start': pyglet.image.load('resources/main_menu.jpg'),
            'background': pyglet.image.load('objects/background.png'),
            'cross': pyglet.image.load('objects/cross.png'),
            'cross_disabled': pyglet.image.load('objects/cross.png'),
            'circle': pyglet.image.load('objects/circle.png'),
            'circle_disabled': pyglet.image.load('objects/circle.png'),
            'player_1': pyglet.image.load('objects/player_1.png'),
            'player_2': pyglet.image.load('objects/player_2.png'),
            'undo': pyglet.image.load('objects/undo.png'),
            'undo_disabled': pyglet.image.load('objects/undo.png'),
            'boards': {
                3: pyglet.image.load('objects/board_3.png')
            }
        }

        # Set Active Screen
        self.showing = 'game'
        self.playing = False
        self.engine = engine
        self.sprites = {}

    @property
    def width(self):
        return self.get_size()[0]

    @property
    def height(self):
        return self.get_size()[1]

    def on_draw(self):
        self.clear()
        canvas, self.sprites = None, {}
        if self.showing == 'start':
            canvas = pyglet.sprite.Sprite(self.images['start'], x=0, y=0)
            canvas.scale = max(min(canvas.height, self.height)/max(canvas.height, self.height), min(canvas.width, self.width)/max(canvas.width, self.width))
            
        elif self.showing == 'game':
            canvas = pyglet.sprite.Sprite(self.images['background'], x=0, y=0)

            board = Board(3, (self.width / 2), (self.height / 2))
            undo = Button('undo')
            undo.x = (board.x + board.width) - undo.width
            undo.y = board.y + board.height + 5
            player = Button('player_1')
            player.x = board.x
            player.y = board.y + board.height + 5
            end = Button('end')
            end.x = (self.width / 2) - (end.width / 2)
            end.y = board.y - end.height - 5

            self.sprites['board'] = board
            self.sprites['undo'] = undo
            self.sprites['player'] = player
            self.sprites['end'] = end
            
        canvas.draw()

        for name, obj in self.sprites.items():
            obj.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        print(f'Mouse Pressed: {x} {y}')
        if self.showing == 'start':
            if x in range(200, 630) and y in range(315, 350):
                print('Collided with Rules: 3x3')
                self.rules('3x3')
            elif x in range(180, 630) and y in range(230, 265):
                self.rules('Flip')
            elif x in range(100, 700) and y in range(150, 190):
                self.rules('Ulti')
            elif ((x in range(100, 220) and y in range(45, 70)) or
                  (x in range(80, 235) and y in range(70, 105))):
                self.load()

        elif self.showing == 'game':
            for item, obj in self.sprites.items():
                if hasattr(obj, 'collide') and obj.collide(x, y):
                    print(f'Collided with {item}')
            
        elif self.showing == 'Rules':
            if (((x-380)**2)/10) + (((y-90)**2)/5) <= 25**2:
                self.board(self.currentscreen[1])
            elif ((x in range(560, 760) and y in range(480, 500)) or
                  (x in range(610, 720) and y in range(500, 545))):
                self.main()

        elif self.showing == 'Board':
            """Board Clicking"""
            print(f'You clicked inside the board! {x} {y}')
            if ((x in range(45, 243) and y in range(48, 62)) or
                    (x in range(80, 180) and y in range(62, 110))):
                print('You clicked inside the board! ')
                self.save(self.currentscreen)

    @staticmethod 
    def show():
        pyglet.app.run()

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
            self.playing = True
        elif mode == 'Flip':
            self.background = pyglet.image.load('resources/flip_game.jpg')
        elif mode == 'Ulti':
            self.background = pyglet.image.load('resources/ultimate_game.jpg')

window = Interface(Game(TicTacToe()))
window.show()