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
    # Current Player
    player = 1
    # Winner
    winner = None    
    # Prompt the Player to Flip
    flip = False

    while True:
        # Set up the screen
        clear()
        banner()
        status('Flip Mode', player)
        print('')
        
        # Print board
        _board = tb.DoubleTable(board.matrix)
        _board.inner_heading_row_border = False
        _board.inner_row_border = True
        print(_board.table)
        print('')

        # Check if there are still movable pieces, otherwise end the game
        if board.over():
            break

        # Prompt player for input
        prompt = 'Flip: <row>, <column>, <direction (u,d,l,r)>' if flip else 'Move: <row>, <column>'
        inpt = [args.strip() for args in input(f'{prompt} | <quit> : ').split(',')]

        # If user typed 'quit', exit to main menu
        if inpt[0] == 'quit':
            break

        # Check if input should be parsed as flip or set
        if flip:
            if len(inpt) == 3:
                flipped = board.flip(int(inpt[0]), int(inpt[1]), inpt[2])

                # Check if flip successful
                if flipped:
                    # Check for winners
                    if board.check(flipped[0], flipped[1]):
                        winner = 1 if player == 2 else 2
                        break
                    # Next move should be set
                    flip = False
                else:
                    # Flip failed, try again
                    continue
            else:
                # Incomplete input, try again
                continue
        else:
            if len(inpt) == 2:
                move = board.set('x' if player == 1 else 'o', int(inpt[0]), int(inpt[1]))

                # Check if set is successful
                if move:
                    # Check for winners
                    if board.check(int(inpt[0]), int(inpt[1])):
                        winner = player
                        break
                    # Change current player
                    player = 1 if player == 2 else 2
                    # Next move should be flip
                    flip = True
                else:
                    # Action failed, try again
                    continue
            else:
                # Incomplete input, try again
                continue
    
    # Show game over screen
    end(winner)

def ulimate():
    """Play Ultimate Mode"""
    B = UltimateMode()

    locked = False
    player = 1
    ctr = 0

    while True:        
        # Set up screen
        clear()
        banner()
        status('Ultimate Mode', player)
        print('')

        # Print board
        B.string()

        # Prompt player for input
        prompt = 'Select Board <x>, <y>' if not locked else 'Move <row>, <column>'
        inp = [args.strip() for args in input(f'{prompt} | <quit> : ').split(',')]
        
        # If user typed 'quit', exit to main menu
        if inp[0] == 'quit':
            break

        # If incomplete input, try again
        if len(inp) != 2:
            continue
        
        # If board is not locked, parse input as board coordinates
        if not locked:
            x, y = int(inp[0]), int(inp[1])
            locked = True
            continue
        else:
            # else, parse input as cell coordinates
            ix, iy = int(inp[0]), int(inp[1])

        if B.get(x, y, ix, iy) == ' ':
            value = 'x' if player == 1 else 'o'
            B.set(value, x, y, ix, iy)

            check = B.check(x, y, ix, iy)
            if check != False:
                B.set(check[0], x, y)

                check = B.check(x, y)
                if check != False:
                    print('\n')
                    if check[0] == '-':
                        end(None)
                    elif check[0] == 'x':
                        end('1')
                    else:
                        end('2')
                    break

            if B.big[ix][iy] == ' ':
                locked = True
                x, y = ix, iy
            else:
                locked = False

            # Change player
            player = 1 if player == 2 else 2

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
        elif action == '2':
            ulimate()



