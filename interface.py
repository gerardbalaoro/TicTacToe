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
            'background': pyglet.image.load('images/background.png'),
            'background_dark': pyglet.image.load('images/background_dark.png'),
            'background_light': pyglet.image.load('images/background_light.png'),
            'player_1': pyglet.image.load('images/player_1.png'),
            'player_2': pyglet.image.load('images/player_2.png'),
            'icon_32': pyglet.image.load('images/icon_32.png'),
            'icon_16': pyglet.image.load('images/icon_16.png'),
        }

        self.set_icon(self.images['icon_32'], self.images['icon_16'])

        # Game Instance, access engine using `self.game.engine`
        self.game = game

        # Drawable Windows Elements
        self.drawables = {}
        self.shown = None

        # Set Initial Screen
        self.start_screen()

    @staticmethod 
    def show():
        """Show Game Window"""
        pyglet.app.run()

    @staticmethod
    def close():
        """Close Game Window"""
        pyglet.app.exit()

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

        if self.showing == 'start':
            self.controls['load'].disabled = not self.game.has_save()

        elif self.showing == 'game':
            for _btn in ['end', 'undo']:
                if not self.controls[_btn].focused:
                    self.controls[_btn].disabled = not self.game.finished_move
                    if _btn == 'undo' and self.mode == FlipTacToe and self.game.finished_flip and self.game.round != 1:
                        self.controls[_btn].disabled = False
            
            self.board.clear_tiles()
            for row, items in enumerate(self.game.engine.items):
                for col, value in enumerate(items):
                    if value != ' ':
                        self.board.add_tile('cross' if value.lower() == 'x' else 'circle', row, col, value.isupper())
            self.drawables['tiles'] = self.board.tiles

            if self.mode == TicTacToe:
                self.controls['panel'].set_image('info_undo' if self.game.finished_move else 'info_help')
            if self.mode == FlipTacToe:
                if not self.game.finished_flip:
                    self.controls['panel'].set_image('flip_panel')
                    if self.game.to_flip is None:
                        self.controls['panel'].focused = False
                    else:
                        self.controls['panel'].focused = True
                else:
                    self.controls['panel'].set_image('info_undo' if self.game.finished_move else 'info_help')

        _render(self.drawables)
        self.shown = self.showing
   
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle Mouse Press Events"""
        if self.shown in ['game', 'end']:
            for name, elem in self.controls.items():
                if elem.collide(x, y) is not False and not elem.disabled:
                    elem.focused = True

    def on_mouse_release(self, x, y, button, modifiers):
        """Hande Mouse Release Events"""            
        if self.shown in ['start', 'game', 'end']:
            for name, elem in self.controls.items():
                if elem.collide(x, y) is not False and not elem.disabled:
                    if self.shown == 'start':
                        if name == 'classic':
                            self.game.new(TicTacToe())
                            self.game_screen()
                        elif name == 'flip':
                            self.game.new(FlipTacToe())
                            self.game_screen()
                        elif name == 'load':
                            self.game.load()
                            self.game_screen()
                        elif name == 'exit':
                            self.close()
                    elif self.shown == 'game':
                        if name == 'end':
                            if self.game.winner is not None or self.game.engine.over():
                                self.end_screen()                            
                            else:
                                self.game.player_end_turn()
                                self.controls['player'].image = self.images['player_' + str(self.game.player)]
                        elif name == 'undo':
                            self.game.player_undo_move()                        
                        elif name == 'quit':
                            self.start_screen()
                        elif name == 'save':
                            self.game.save()
                    elif self.shown == 'end':
                        if name == 'continue':
                            self.start_screen()
                    elem.focused = False
            
            if self.shown == 'game':
                collision = self.board.collide(x, y)
                if isinstance(collision, tuple):
                    r, c = collision

                    # Vanilla Mode
                    if self.mode == TicTacToe:
                        if not self.game.finished_move:
                            if self.game.engine.set(self.game.player_tile, r, c):
                                self.game.player_end_move()
                                if self.game.engine.check(r, c):
                                    self.game.winner = self.game.player
                    
                    # Flip Mode
                    elif self.mode == FlipTacToe:
                        if not self.game.finished_flip:
                            if self.game.to_flip is not None:
                                if self.game.to_flip == (r, c):
                                    self.drawables['tiles']['{},{}'.format(r, c)].focused = False
                                    self.game.to_flip = None
                                    self.board.clear_arrows()                                  
                                else:
                                    flippable = self.game.engine.canflip(*self.game.to_flip, True)
                                    for d, coor in flippable.items():                                        
                                        if (r, c) == coor:
                                            flip = self.game.engine.flip(*self.game.to_flip, d)
                                            if flip is not False:
                                                self.game.player_end_flip()
                                                if self.game.engine.check(r, c):
                                                    self.game.winner = self.game.other_player
                                                self.board.clear_arrows()
                                                break                                                                               
                            else: 
                                if not self.game.is_player_piece(r, c):                             
                                    flippable = self.game.engine.canflip(r, c, True)                                
                                    if len(flippable) > 0:
                                        self.game.to_flip = (r, c)                                    
                                        self.drawables['tiles']['{},{}'.format(r, c)].focused = True
                                        self.board.clear_arrows()
                                        for d, (_r, _c) in flippable.items():
                                            self.board.add_arrow(d, _r, _c)
                            self.drawables['arrows'] = self.board.arrows
                        elif not self.game.finished_move:
                            if self.game.engine.set(self.game.player_tile, r, c):
                                self.game.player_end_move()
                                if self.game.engine.check_unflippable(r, c):
                                    self.game.winner = self.game.player                       
                            else:
                                print('Game Error: Set Returned False')
      
    def start_screen(self):    
        """Render Start Screen Elements"""
        self.canvas = pyglet.sprite.Sprite(self.images['background_light'], x=0, y=0)

        # Controls
        self.controls = {
            'title': Button('title'),
            'subtitle': Button('subtitle'),
            'classic': Button('classic'),
            'flip': Button('flip'),
            'load': Button('load'),
            'exit': Button('exit')
        }

        self.controls['title'].x = (self.width / 2) - (self.controls['title'].width / 2)
        self.controls['title'].y = (self.height * 0.70) 
        self.controls['subtitle'].x = (self.width / 2) - (self.controls['subtitle'].width / 2)
        self.controls['subtitle'].y = self.controls['title'].y - self.controls['subtitle'].height - 30

        buttons = ['classic', 'flip', 'load', 'exit']
        for i, name in enumerate(buttons):
            self.controls[name].x = (self.width / 2) - (self.controls[name].width / 2)
            self.controls[name].y = (self.height * 0.45) - (self.controls[name].height * (i + 1)) - (10 * i)
        self.controls['exit'].y -= 30

        self.drawables = {'canvas': self.canvas, 'controls': self.controls}
        self.showing = 'start'

    def end_screen(self):
        """Render Game Over Screen Elements"""
        self.canvas = pyglet.sprite.Sprite(self.images['background_light'], x=0, y=0)

        # Controls
        self.controls = {
            'title': Button('game_over'),
            'continue': Button('continue'),
            'winner': Button('winner_{}'.format(self.game.winner) if self.game.winner is not None else 'draw')
        }

        self.controls['title'].x = (self.width / 2) - (self.controls['title'].width / 2)
        self.controls['title'].y = (self.height * 0.60) 
        self.controls['winner'].x = (self.width / 2) - (self.controls['winner'].width / 2)
        self.controls['winner'].y = (self.height / 2)
        self.controls['continue'].x = (self.width / 2) - (self.controls['continue'].width / 2)
        self.controls['continue'].y = (self.height * 0.30)

        self.drawables = {'canvas': self.canvas, 'controls': self.controls}
        self.showing = 'end'

    def game_screen(self):
        """Render Game Screen Elements"""
        self.mode = type(self.game.engine)
        self.canvas = pyglet.sprite.Sprite(self.images['background'], x=0, y=0)

        # Board
        self.board = Board(self.game.engine.size, (self.width / 2), (self.height / 2), tilesize=74 if self.mode == FlipTacToe else None)

        # Controls
        self.controls = {
            'undo': Button('undo'),
            'end': Button('end'),
            'player': Button('player_{}'.format(self.game.player)),
            'quit': Button('quit'),
            'save': Button('save'),
            'panel': Button('info_help', self.width * 0.10, self.board.y)
        }

        self.controls['undo'].x = (self.board.x + self.board.width) - self.controls['undo'].width
        self.controls['undo'].y = (self.board.y + self.board.height) + 5
        self.controls['undo'].disabled, self.controls['end'].disabled = True, True
        self.controls['player'].x = self.board.x
        self.controls['player'].y = self.board.y + self.board.height + 5
        self.controls['end'].x = (self.width / 2) - (self.controls['end'].width / 2)
        self.controls['end'].y = self.board.y - self.controls['end'].height - 5
        self.controls['quit'].x = self.width - self.controls['quit'].width - 20
        self.controls['quit'].y = self.height - 20 - self.controls['quit'].height
        self.controls['save'].x = self.width - self.controls['save'].width - 20
        self.controls['save'].y = self.height - 20 - (self.controls['save'].height * 2) - 10
        self.drawables = {'canvas': self.canvas, 'board': self.board, 'controls': self.controls}
        self.showing = 'game'