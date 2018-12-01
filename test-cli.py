import terminaltables as tb, os
from argparse import ArgumentParser
from engine import *

def clear():
    """Clear console"""
    _cls = os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    """Print Game Banner"""
    print(tb.DoubleTable(['TICTACTOE']).table)

def start():
    """Show Game Start Menu"""
    selected = None
    modes = {'1': 'Play Flip Mode', '2': 'Play Ultimate Mode', 'Q': 'Quit Game'}
    while selected not in modes.keys():
        clear()
        banner()
        menu = tb.DoubleTable(modes.items())
        menu.inner_heading_row_border = False
        print(menu.table)
        selected = input('Select Option: ')
    return selected

def status(mode, player):
    """Show Game Status"""
    print(tb.DoubleTable([[f'Playing {mode}', f'Player {player}\'s Turn']]).table)

def end(winner = None):
    """Show Game Over Screen"""
    print(tb.DoubleTable([[f'GAME OVER', f'Player {winner} Wins' if winner != None else 'No Winners']]).table)
    input("Press Any Key To Continue")

def flip():
    """Play Flip Mode"""
    board = FlipMode()
    player = 1
    winner = None
    flip = False
    while True:
        clear()
        banner()
        status('Flip Mode', player)
        print('')
        
        _board = tb.DoubleTable(board.matrix)
        _board.inner_heading_row_border = False
        _board.inner_row_border = True
        print(_board.table)

        print('')
        if board.over():
            break

        prompt = 'Flip: <row>, <column>, <direction (u,d,l,r)>' if flip else 'Move: <row>, <column>'
        move = [args.strip() for args in input(f'{prompt} | <quit> : ').split(',')]
        if move[0] == 'quit':
            break

        if flip:
            if len(move) == 3:
                flipped = board.flip(int(move[0]), int(move[1]), move[2])
                if flipped:
                    if board.check(flipped[0], flipped[1]):
                        winner = 1 if player == 2 else 2
                        break
                    flip = False
                else:
                    continue
            else:
                continue
        else:
            if len(move) == 2:
                board.set('x' if player == 1 else 'o', int(move[0]), int(move[1]))

                if board.check(int(move[0]), int(move[1])):
                    winner = player
                    break     
                player = 1 if player == 2 else 2
                flip = True
            else:
                continue
    end(winner)

def ulimate():
    """Play Ultimate Mode"""
    pass

#: ---------------------------
#: Main Game Runner
#: ---------------------------
if __name__ == '__main__':
    # Activate Debugger (Local Environment Only)
    p = ArgumentParser()
    p.add_argument('--debug', '-p', type=bool, default=False)
    args = p.parse_args()
    if args.debug == True:
        import ptvsd
        print("Waiting for debugger attach")
        ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
        ptvsd.wait_for_attach()

    # Start Game
    while True:
        action = start()        
        if action == 'Q':            
            break
        elif action == '1':
            flip()



