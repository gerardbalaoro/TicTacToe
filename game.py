from engine import *
from session import *

class Game:
    """Wrapper for Engine and Session Class"""

    def __init__(self, symbols=('x', 'o')):
        """Initialize Instance
        
        Arguments:
            symbols {tuple} -- player symbols (default: {('x', 'o')})
        """
        self.players = dict(zip((1, 2), players))

    def new(self, engine:TicTacToe=None):
        """Start New Game
        
        Arguments:
            engine {TicTacToe} -- game engine instance
        """
        self.player = 1
        self.engine = engine
        self.session = Session()
        self.winner = None
        self.player_start_turn()

    @property
    def player_tile(self):
        """Get Current Player Symbol"""
        return self.players[self.player]

    def player_start_turn(self):
        """Start Current Player Turn"""
        self.engine.capture()
        self.finished_move = False

    def player_end_move(self):
        """End Current Player Turn"""
        self.engine.savesnap()
        self.finished_move = True

    def player_undo_move(self):
        """Undo Current Player's Last Move"""
        self.engine.restore()
        self.player_start_turn()

    def player_end_turn(self):
        """End Current Player Turn"""
        self.player = 2 if self.player == 1 else 1
        self.player_start_turn()