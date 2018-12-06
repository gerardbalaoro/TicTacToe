"""Game Engine Module"""

import terminaltables as tb
from copy import deepcopy

class TicTacToe:
    """Vanilla TicTacToe Class"""

    snapshots = []
    clipboard = None

    def __init__(self, size=3):
        """Initialize board matrix
        
        Arguments:
            size {int} -- length of board sides (default: {3})
        """
        self.matrix = [[' '] * size for row in range(size)]        

    @property
    def items(self):
        """Get a copy of the current board items
        
        Returns:
            list
        """
        return deepcopy(self.matrix)

    @property
    def board(self):
        """Get printable representation of the current board state"""
        _board = tb.DoubleTable(self.matrix)
        _board.inner_heading_row_border = False
        _board.inner_row_border = True
        return _board.table

    @board.deleter
    def board(self):
        """Reset board"""
        self.matrix = [[' '] * self.size for row in range(self.size)]
    
    @property
    def size(self):
        """Get length of game board sides

        Returns:
            int
        """
        return len(self.matrix)

    def row(self, n):
        """Get row values

        Parameters:
            n {int} -- a zero based row number

        Returns:
            tuple
        """
        return tuple(self.matrix[n])

    def column(self, n):
        """Get column values
        
        Parameters:
            n {int} -- a zero based row number
        
        Returns:
            tuple
        """
        return tuple([row[n] for row in self.matrix])

    def diagonals(self, r, c, coordinates=False):
        """Get diagonal values intersecting (r, c) coodinates

        Parameters:
            r {int} -- a zero based row number
            c {int} -- a zero based column number
            coodinates {bool} -- returns cell coordinates instead of values

        Returns:
            dict -- forward and backward diagonal values
        """
        forwards = []
        backwards = []

        for x in range(self.size):
            y = (x - r) + c
            if y in range(self.size):
                if coordinates:
                    forwards.append((x, y))
                else:
                    forwards.append(self.get(x, y))

            y = (r - x) + c
            if 0 <= y < self.size:
                if coordinates:
                    backwards.append((x, y))
                else:
                    backwards.append(self.get(x, y))

        return {'forward': tuple(forwards), 'backward': tuple(backwards)}        

    def get(self, r, c):
        """Get cell value
        
        Parameters:
            r {int} -- zero-based row number
            c {int} -- zero-based column number
        
        Returns:
            mixed -- value {str}, False {bool} if (r, c) does not exist
        """
        if 0 <= r < self.size and 0 <= c < self.size:
            return self.matrix[r][c]
        else:
            return False

    def set(self, value, r, c, force=False):
        """Set cell value
        
        Parameters:
            value {str} -- value to assign
            r {int} -- zero-based row number
            c {int} -- zero-based column number
            force {bool} -- overwrite value on non-empty cells
        
        Returns:
            bool -- True on success, False on fail
        """
        if 0 <= r < self.size and 0 <= c < self.size and (force == True or self.get(r, c) == ' '):
            self.matrix[r][c] = value
            return True
        else:
            return False

    def check(self, r, c):
        """Check if (r, c) value exists at least three times consecutively lines in any direction (horizontal, vertical, diagonal)
        intersecting with (r, c)
        
        Parameters:
            r {int} -- zero-based row number
            c {int} -- zero-based column number
        
        Returns:
            bool
        """        
        value = self.get(r, c)

        if str(value * 3) in ''.join(self.row(r)):
            return True

        if str(value * 3) in ''.join(self.column(c)):
            return True            

        for direction, values in self.diagonals(r, c).items():
            if str(value * 3) in ''.join(values):
                return True

        return False

    def over(self):
        """Check if there are no more moves left

        Returns:
            bool
        """
        for _r in range(self.size):
            if self.row(_r).count(' ') > 0:
                return False
        
        return True

    def capture(self):
        """Capture current board state to clipboard"""
        self.clipboard = deepcopy(self.matrix)

    def savesnap(self):
        """Save current clipboard contents to snapshots"""
        if self.clipboard != None and self.clipboard not in self.snapshots:
            self.snapshots.append(deepcopy(self.clipboard))
            self.clipboard = None

    def restore(self, index=-1):
        """Restores a snapshot of the board
        
        Arguments:
            index {int} -- snapshot index (default: {-1})
        """
        try:
            self.matrix = deepcopy(self.snapshots[index])
            del self.snapshots[index]
        except IndexError:
            pass

class FlipTacToe(TicTacToe):
    """FlipTacToe Board Class"""

    def __init__(self, size=4):
        """Initialize board matrix"""
        super().__init__(size)

    def flip(self, r, c, d, force=False):
        """Flip cell in one of the 4 cardinal directions
        
        Parameters:
            r {int} -- zero-based row number
            c {int} -- zero-based column number
            d {str} -- flip direction, (u, d, l, r)
            force {bool} -- overwrite value on non-empty cells

        Returns:
            mixed -- (r, c) coordinates of flipped cell, False on fail
        """
        value = self.get(r, c)

        if value.islower():
            value = value.upper()
        else:
            value = value.lower()

        d = d.lower()[0]

        if d in self.canflip(r, c) or force is True:
            self.set(' ', r, c, True)

            if d == 'u':   
                r -= 1         
            elif d == 'd':
                r += 1
            elif d == 'l':
                c -= 1
            elif d == 'r':
                c += 1

            if self.set(value, r, c, force):
                return r, c

        return False

    def canflip(self, r, c, coordinates=False):
        """Check if the cell value can still be flipped
        
        Parameters:
            r {int} -- zero-based row number
            c {int} -- zero-based column
            coordinates {bool} -- return flippable directions coordinates 
            
        Returns:
            tuple/dict -- directions cell can be flipped to
        """
        directions = {
            'u': (r - 1, c),
            'd': (r + 1, c),
            'l': (r, c - 1),
            'r': (r, c + 1),
        }

        flippable = []
        cells = {}

        if self.get(r, c) == ' ':
            return False

        for d, (_r, _c) in directions.items():
            if self.get(_r, _c) == ' ':
                flippable.append(d)
                cells[d] = (_r, _c)

        return cells if coordinates else tuple(flippable)

    def check_unflippable(self, r, c):
        """Check if (r, c) value exists at least three times consecutively lines in any direction (horizontal, vertical, diagonal)
        intersecting with (r, c) and if all cells in that direction can no longer be flipped
        
        Parameters:
            r {int} -- zero-based row number
            c {int} -- zero-based column number
        
        Returns:
            bool
        """
        value = self.get(r, c)
        size = self.size

        if str(value * 3) in ''.join(self.row(r)):
            for y in range(size):
                if len(self.canflip(r, y)) != 0:
                    return False
            return True

        if str(value * 3) in ''.join(self.column(c)):
            for x in range(size):
                if len(self.canflip(x, c)) != 0:
                    return False
            return True           

        for direction, coordinates in self.diagonals(r, c, True).items():
            if str(value * 3) in ''.join([self.get(x, y) for x, y in coordinates]):
                for x, y in coordinates:
                    if len(self.canflip(x, y)) != 0:
                        return False
                return True

        return False
