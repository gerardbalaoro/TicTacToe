"""Main Module"""

from interface import *
from engine import *
from session import *

class Game:
    """Wrapper for Engine and Session Class"""

    def __init__(self, symbols=('x', 'o')):
        """Initialize Instance
        
        Arguments:
            symbols {tuple} -- player symbols (default: {('x', 'o')})
        """
        self.players = dict(zip((1, 2), symbols))
        self.session = Session()

    def new(self, engine:TicTacToe=None):
        """Start New Game
        
        Arguments:
            engine {TicTacToe} -- game engine instance
        """
        self.player = 1
        self.round = 1
        self.engine = engine
        self.session = Session()
        self.winner = None
        self.player_start_turn()

    @property
    def player_tile(self):
        """Get Current Player Symbol"""
        return self.players[self.player]

    @property
    def other_player(self):
        """Get Other Player"""
        return 2 if self.player == 1 else 1

    @property
    def other_tile(self):
        """Get Oter Player Symbol"""
        return self.players[self.other_player]

    def player_start_turn(self):
        """Start Current Player 
        
        Arguments:
            new {bool} -- new game
        """
        self.engine.capture()
        self.finished_move = False
        self.finished_flip = True if self.round == 1 else False
        self.to_flip = None

    def player_end_move(self):
        """End Current Player Turn"""
        self.engine.savesnap()
        self.finished_move = True

    def player_end_flip(self):
        """End Current Player Flip (for FlipTacToe)"""
        self.engine.savesnap()
        self.to_flip = None
        self.finished_flip = True

    def player_undo_move(self):
        """Undo Current Player's Last Move"""
        self.engine.restore()
        self.player_start_turn()

    def player_end_turn(self):
        """End Current Player Turn"""
        self.player = self.other_player
        self.round += 1
        self.player_start_turn()

    def is_player_piece(self, r, c):
        """Check if Tile Belongs to Current Player
        
        Arguments:
            r {int} -- zero-based row number
            c {int} -- zero-based column number

        Returns:
            bool
        """
        return self.engine.get(r, c).lower() == self.player_tile

    def has_save(self, name='latest'):
        """Save Game Session
        
        Arguments:
            name {str} -- save file name
        
        Returns:
            bool
        """
        return self.session.savfile(name, find=True)

    def save(self, name='latest'):
        """Save Game Session
        
        Arguments:
            name {str} -- save file name
        """
        self.session.load({
            'player': self.player,
            'winner': self.winner,
            'board': {
                'type':type(self.engine).__name__,
                'size': self.engine.size,
                'matrix': self.engine.matrix,
                'snapshots': self.engine.snapshots,
                'clipboard': self.engine.clipboard
            },
            'round': self.round,
            'memory': {
                'flip': self.finished_flip,
                'move': self.finished_move,
                'lock': self.to_flip
            }
        })

        self.session.write(name)

    def load(self, name='latest'):
        """Load Game Session

        Arguments:
            name {str} -- save file name
        """
        self.session.read(name)
        loaded = self.session.data
        self.player = loaded['player']
        self.winner = loaded['winner']
        self.engine = eval(loaded['board']['type'])(loaded['board']['size'])
        self.engine.matrix = loaded['board']['matrix']
        self.engine.snapshots = loaded['board']['snapshots']
        self.engine.clipboard = loaded['board']['clipboard']
        self.round = loaded['round']
        self.finished_flip = loaded['memory']['flip']
        self.finished_move = loaded['memory']['move']
        self.to_flip = loaded['memory']['lock']

# Start Game if Script is run directly
if __name__ == '__main__':
    game = Game()
    window = Interface(game)
    window.show()