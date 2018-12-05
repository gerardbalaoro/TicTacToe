import pyglet
from pyglet.gl import *
from objects import *
from game import *

class Interface(pyglet.window.Window):
    def __init__(self, game:Game):
        """Initialize Game Interface
        
        Arguments:
            game {Game} -- Game class instance
        """
        super().__init__(width=800, height=600, caption='Tic Tac Toe Unlimited', resizable=False)
        
        # Game Image Assets
        self.images = {
            'start': pyglet.image.load('resources/main_menu.jpg'),
            'background': pyglet.image.load('images/background.png'),
            'player_1': pyglet.image.load('images/player_1.png'),
            'player_2': pyglet.image.load('images/player_2.png'),
        }

        # Mouse Cursors
        self.cursors = {
            'disabled': self.get_system_mouse_cursor(self.CURSOR_NO),
            'default': self.get_system_mouse_cursor(self.CURSOR_DEFAULT),
            'hand': self.get_system_mouse_cursor(self.CURSOR_HAND)            
        }

        # Game Instance, access engine using `self.game.engine`
        self.game = game

        # Drawable Windows Elements
        self.drawables = {}

        # Set Initial Screen
        self.start_screen()

    @staticmethod 
    def show():
        """Show Game Window"""
        pyglet.app.run()

    @property
    def width(self):
        """Get Window Width
        
        Returns:
            int
        """
        return self.get_size()[0]

    @property
    def height(self):
        """Get Window Height
        
        Returns:
            int
        """
        return self.get_size()[1]

    def on_draw(self):
        """Render Drawable Elements on Screen"""
        self.clear()

        def _render(item):
            if isinstance(item, pyglet.sprite.Sprite):
                item.draw()
            elif isinstance(item, dict):
                for subitem, obj in item.items():
                    _render(obj)
            elif isinstance(item, (list, tuple)):
                for subitem in item:
                    _render(subitem)

        _render(self.drawables)
        self.shown = self.showing
   
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle Mouse Press Events"""

        # NOTE: For Debug Only, Print Mouse Coordinates
        print('Mouse Pressed: {} {} | On Screen: {}'.format(x, y, self.shown))

        # Start Screen Mouse Events
        if self.shown == 'start':
            
            if x in range(200, 630) and y in range(315, 350):
                print('Selected Vanilla TicTacToe')
                self.game.new(TicTacToe())
                self.help_screen()
                
            elif x in range(180, 630) and y in range(230, 265):
                print('Selected FlipTacToe')
                self.game.new(FlipTacToe())
                self.help_screen()

            elif x in range(100, 700) and y in range(150, 190):
                print('Selected Ultimate TicTacToe')
                self.game.new(UltimateTicTac())
                self.help_screen()

            elif ((x in range(100, 220) and y in range(45, 70)) or
                  (x in range(80, 235) and y in range(70, 105))):
                pass

        # In-Game Screen Mouse Events
        elif self.shown == 'game':

            # Check if a Control is Clicked
            for name, elem in self.controls.items():
                if elem.collide(x, y) is not False and not elem.disabled:
                    print('Button Pressed: {}'.format(name))
                    elem.focused = True
                    if name == 'end':
                        if self.game.winner is not None:
                            print('Game Over: Player {} Won'.format(self.game.winner))
                        else:
                            self.game.player_end_turn()
                            self.controls['player'].image = self.images['player_' + str(self.game.player)]
                    elif name == 'undo':
                        self.game.player_undo_move()
                        self.board.clear_tiles()
                        for row, items in enumerate(self.game.engine.items):
                            for col, value in enumerate(items):
                                if value != ' ':
                                    self.board.add_tile('cross' if value == 'x' else 'circle', row, col)
                        self.drawables['tiles'] = self.board.tiles
                        self.controls['undo'].disabled = True
                        self.controls['end'].disabled = True

            # Vanilla Mode
            if self.mode == TicTacToe:
                onboardclick = self.board.collide(x, y)
                if isinstance(onboardclick, tuple) and self.game.finished_move is False:
                    r, c = onboardclick
                    print('Board Cell Clicked: {}, {}'.format(onboardclick[0], c))
                    if self.game.engine.set(self.game.player_tile, r, c):                    
                        self.board.add_tile('cross' if self.game.player_tile == 'x' else 'circle', r, c)                
                        self.drawables['tiles'] = self.board.tiles
                        self.game.player_end_move()
                        self.controls['undo'].disabled = False
                        self.controls['end'].disabled = False

                        if self.game.engine.check(r, c):
                            self.game.winner = self.game.player                        
                    else:
                        print('Game Error: Set Returned False')
            
            # Flip Mode
            elif self.mode == FlipTacToe:
                pass
            
            # Ultimate Mode
            elif self.mode == UltimateTicTac:
                pass
            
        # Help Screen Mouse Events
        elif self.shown == 'help':
            
            if x in range(339, 436) and y in range(85, 115):
                print('Button Clicked: play')                
                self.game_screen()

            elif ((x in range(560, 760) and y in range(480, 500)) or
                  (x in range(610, 720) and y in range(500, 545))):
                self.start_screen()

    def on_mouse_release(self, x, y, button, modifiers):
        """Hande Mouse Release Events"""
        if self.shown == 'game':
            for name, elem in self.controls.items():
                if elem.collide(x, y) is not False and not elem.disabled:
                    elem.focused = False

    def start_screen(self):    
        """Render Start Screen Elements"""
        self.canvas = pyglet.sprite.Sprite(self.images['start'], x=0, y=0)
        self.canvas.scale = max(min(self.canvas.height, self.height)/max(self.canvas.height, self.height), min(self.canvas.width, self.width)/max(self.canvas.width, self.width))
        self.drawables = [self.canvas]
        self.showing = 'start'

    def game_screen(self):
        """Render Game Screen Elements"""
        self.canvas = pyglet.sprite.Sprite(self.images['background'], x=0, y=0)

        # Board
        self.board = Board(3, (self.width / 2), (self.height / 2))

        # Controls
        self.controls = {
            'undo': Button('undo'),
            'end': Button('end'),
            'player': Button('player_{}'.format(self.game.player))
        }

        self.controls['undo'].x = (self.board.x + self.board.width) - self.controls['undo'].width
        self.controls['undo'].y = (self.board.y + self.board.height) + 5
        self.controls['undo'].disabled = not self.game.finished_move
        self.controls['player'].x = self.board.x
        self.controls['player'].y = self.board.y + self.board.height + 5
        self.controls['end'].x = (self.width / 2) - (self.controls['end'].width / 2)
        self.controls['end'].y = self.board.y - self.controls['end'].height - 5
        self.controls['end'].disabled = not self.game.finished_move

        self.drawables = {'canvas': self.canvas, 'board': self.board, 'controls': self.controls}
        self.showing = 'game'

    def help_screen(self):
        """Render Help Screen Elements"""   
        self.mode = type(self.game.engine)
        if self.mode == TicTacToe:
            self.canvas = pyglet.image.load('resources/rules_3x3.jpg')
        elif self.mode == FlipTacToe:
            self.canvas = pyglet.image.load('resources/rules_flip.jpg')
        elif self.mode == UltimateTicTac:
            self.canvas = pyglet.image.load('resources/rules_ultimate.jpg')
        self.canvas = pyglet.sprite.Sprite(self.canvas)
        self.canvas.scale = max(min(self.canvas.height, self.height)/max(self.canvas.height, self.height), min(self.canvas.width, self.width)/max(self.canvas.width, self.width))
        self.drawables = [self.canvas]
        self.showing = 'help'