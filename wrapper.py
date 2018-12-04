from engine import *
from session import *

class Game:
    """Wrapper for Engine Class"""

    players = {1: 'x', 2: 'o'}
    running = True
    playing = False
    engine = None
    current_player = players[1]
    winner = None
    session = Session()

    def __init__(self, engine:TicTacToe, players=('x', 'o')):
        self.engine = engine
        self.players[1], self.players[2] = players

    def __call__(self):
        return self.engine

class InvalidMove(Exception):
    """Invalid Move Event"""

    def __init__(self, message=None):
        super().__init__(message if message == None else "Event Raised - Invalid Move")

class GameOver(Exception):
    """Game Over Event"""

    def __init__(self, message=None):
        super().__init__(message if message == None else "Event Raised - Game Over")