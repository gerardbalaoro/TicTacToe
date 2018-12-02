import terminaltables as tb
from copy import deepcopy

class TicTacToe:
    """Vanilla TicTacToe Class"""

    def __init__(self, size=3):
        """Initialize board matrix
        
        Arguments:
            size {int} -- length of board sides (default: {3})
        """
        self.matrix = [[' '] * size for row in range(size)]
        self.history = []
        self.snapshots = []
        self.clipboard = None

    @property
    def board(self):
        """Return a printable representation of the current board state"""
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
            if 0 <= y < self.size:
                if coordinates:
                    forwards.append((x, y))
                else:
                    forwards.append(self.get(x, y))

            y = (r + x) + c
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
            mixed -- cell value, False if (r, c) does not exist
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

    def record(self, action, *args):
        """Record action to history

        Usage:
            self.record('set', 'x', 0, 0)

        Arguments:
            action {str} -- method name
            *args -- variable-length argument list
        """      
        self.history.append({'action': action, 'params': args})

    def replay(self):
        """Replay recorded actions from history"""
        for record in self.history:
            getattr(self, record['action'])(*record['params'])

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
            self.matrix = self.snapshots[index].copy()
        except IndexError:
            pass

class UltimateTicTac(TicTacToe):
    """Ultimate TicTacToe Board Class"""

    def __init__(self):
        """Initialize board matrix"""

        """The actual list of board in each cell"""
        self.matrix = []
        for row in range(3):
            self.matrix.append([])
            for col in range(3):
                inner_board = []
                for inner_row in range(3):
                    inner_board.append([' ']*3)
                self.matrix[row].append(inner_board)

        """
        A summarized version of the main board that will
        only show which of the smaller board are done
        """
        self.big = []
        for row in range(3):
            self.big.append([' ']*3)

    @property
    def board(self):
        """Return a printable representation of the current board state"""
        _master = []
        for _m_row in self.matrix:
            _m_cols = []
            for _m_col in _m_row:
                _i_tb = tb.DoubleTable(_m_col)
                _i_tb.inner_heading_row_border = False
                _i_tb.inner_row_border = True
                _m_cols.append(_i_tb.table)
            _master.append(_m_cols)
        _m_tb = tb.DoubleTable(_master)
        _m_tb.inner_heading_row_border = False
        _m_tb.inner_row_border = True
        return _m_tb.table

    def get(self, x, y, ix=3, iy=3):
        """Get cell value

        Arguments:
            x {int} -- zero-based row number
            y {int} -- zero-based column number

        Returns:
            str
        """
        if ix == 3 or iy == 3:
            return self.big[x][y]
        else:
            return self.matrix[x][y][ix][iy]

    def row(self, n, x=3, y=3):
        """Gets a single row from one of the inner boards or from the main summarized board
        
        Arguments:
            n {int} -- zero-based row number for the inner board
            x {int} -- zero-based row number for the main board
            y {int} -- zero-based column number for the main board
        
        Returns:
            tuple -- elements of the nth row
        """
        if x == 3 or y == 3:
            return tuple(self.big[n])
        else:
            return tuple(self.matrix[x][y][n])

    def column(self, n, x=3, y=3):
        """Gets a single column from one of the inner boards or from the main summarized board
        
        Arguments:
            n {int} -- zero-based column number for the inner board
            x {int} -- zero-based row number for the main board
            y {int} -- zero-based column number for the main board
        
        Returns:
            tuple -- elements of the nth column
        """
        if x == 3 or y == 3:
            return tuple([row[n] for row in self.big])
        else:
            return tuple([row[n] for row in self.matrix[x][y]])

    def set(self, value, x, y, ix=3, iy=3):
        """Sets the cell value based on (x, y, ix, iy) coordinates or just on (x, y) coordinates
        
        Arguments:
            x {int} -- zero-based row number for the main board
            y {int} -- zero-based column number for the main board
            ix {int} -- zero-based row number for the inner board
            iy {int} -- zero-based column number for the inner board
        """
        if ix == 3 or iy == 3:
            if self.get(x, y) == ' ':
                self.big[x][y] = value
        else:
            if self.get(x, y, ix, iy) == ' ':
                self.matrix[x][y][ix][iy] = value

    def check(self, x, y, ix=3, iy=3):
        """Checks if the value existed 3 times vertically, horizontally, or diagonally.
        
        Arguments:
            x {int} -- zero-based row number for the main board
            y {int} -- zero-based column number for the main board
            ix {int} -- zero-based row number for the inner board
            iy {int} -- zero-based column number for the inner board
        
        Returns:
            mixed -- value {str} if a line of 3 is detected, hyphen {str} if draw, else False {bool}.
        """
        if ix == 3 or iy == 3:
            value = self.get(x, y)

            if value != '-':
                if self.row(x).count(value) == 3:
                    return value

                if self.column(y).count(value) == 3:
                    return value

                if self.get(0, 2) == value and self.get(1, 1) == value and self.get(2, 0) == value:
                    return value
                if self.get(0, 0) == value and self.get(1, 1) == value and self.get(2, 2) == value:
                    return value
            else:
                space = 0
                for r in range(3):
                    space += self.big[r].count(' ')
                if space == 0:
                    return '-'
        else:
            value = self.get(x, y, ix, iy)

            if self.row(ix, x, y).count(value) == 3:
                return value

            if self.column(iy, x, y).count(value) == 3:
                return value

            if (self.get(x, y, 0, 2) == value and
                    self.get(x, y, 1, 1) == value and
                    self.get(x, y, 2, 0) == value):
                return value
            if (self.get(x, y, 0, 0) == value and
                    self.get(x, y, 1, 1) == value and
                    self.get(x, y, 2, 2) == value):
                return value

            else:
                space = 0
                for r in range(3):
                    space += self.row(r, x, y).count(' ')
                if space == 0:
                    self.set('-', x, y)
                    return '-'

        return False

class FlipTacToe(TicTacToe):
    """FlipTacToe Board Class"""

    def __init__(self):
        """Initialize board matrix"""
        super().__init__(4)

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

    def canflip(self, r, c):
        """Check if the cell value can still be flipped
        
        Parameters:
            r {int} -- zero-based row number
            c {int} -- zero-based column number
        
        Returns:
            tuple -- directions cell can be flipped to
        """
        directions = {
            'u': (r - 1, c),
            'd': (r + 1, c),
            'l': (r, c - 1),
            'r': (r, c + 1),
        }

        flippable = []

        for d, (_r, _c) in directions.items():
            if self.get(_r, _c) == ' ':
                flippable.append(d)

        return tuple(flippable)

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
