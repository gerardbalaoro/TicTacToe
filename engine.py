class UltimateMode:
    """Ultimate Board Class"""

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

    def string(self):
        """Prints the board in the terminal"""
        out = '-' * 49 + '\n'
        for x in range(3):
            for inner_x in range(3):
                for y in range(3):
                    out += '|  '
                    for inner_y in range(3):
                        if self.get(x, y) != ' ':
                            if inner_y == 0:
                                if inner_x == 1:
                                    out += ' '*5 + self.get(x, y) + ' '*5
                                else:
                                    out += ' '*11
                        else:
                            out += ' {} '.format(self.get(x, y, inner_x, inner_y))
                            if inner_y != 2:
                                out += '|'
                    out += '  '
                out += '|\n'
                for y in range(3):
                    if inner_x != 2:
                        if self.get(x, y) != ' ':
                            out += ('|' + ' '*17)
                        else:
                            out += ('|  ' + '-' * 11 + '  ')
                        if y == 2:
                            out += '|\n'
            out += '-' * 49 + '\n'
        print(out)

    def get(self, x, y, ix=3, iy=3):
        """Get cell value

        Arguments:
            x {int} -- zero-based row number
            y {int} -- zero-based column number

        Returns:
            {str} -- the cell value
        """

        if ix == 3 or iy == 3:
            return self.big[x][y]
        else:
            return self.matrix[x][y][ix][iy]

    def row(self, n, x=3, y=3):
        """
        Gets a single row from one of the inner boards or from the main summarized board
        
        Arguments:
            n {int} -- zero-based row number for the inner board
            x {int} -- zero-based row number for the main board
            y {int} -- zero-based column number for the main board
        
        Returns:
            {tuple} -- contains elements of the nth row
        """
        if x == 3 or y == 3:
            return tuple(self.big[n])
        else:
            return tuple(self.matrix[x][y][n])

    def column(self, n, x=3, y=3):
        """
        Gets a single column from one of the inner boards or from the main summarized board
        
        Arguments:
            n {int} -- zero-based column number for the inner board
            x {int} -- zero-based row number for the main board
            y {int} -- zero-based column number for the main board
        
        Returns:
            {tuple} -- contains elements of the nth column
        """
        if x == 3 or y == 3:
            return tuple([row[n] for row in self.big])
        else:
            return tuple([row[n] for row in self.matrix[x][y]])

    def set(self, value, x, y, ix=3, iy=3):
        """
        Sets the cell value based on (x, y, ix, iy) coordinates or just on (x, y) coordinates
        
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
        """
        Checks if the value existed 3 times vertically, horizontally, or diagonally.
        
        Arguments:
            x {int} -- zero-based row number for the main board
            y {int} -- zero-based column number for the main board
            ix {int} -- zero-based row number for the inner board
            iy {int} -- zero-based column number for the inner board
        
        Returns:
            The value of the line when a line of 3 is detected, a hyphen there is a draw, or False otherwise.
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


class FlipMode:
    """FlipTacToe Board Class"""

    def __init__(self):
        """Initialize board matrix"""
        self.matrix = []
        for row in range(4):
            self.matrix.append([' ']*4)

    def string(self):
        """Print the board in the terminal"""
        print('\n{}\n'.format('-'*15).join(['|'.join([' {} '.format(self.get(x, y))
                                                      for y in range(4)])for x in range(4)]))

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

        for x in range(len(self.matrix)):
            y = (x - r) + c
            if 0 <= y < len(self.matrix):
                if coordinates:
                    forwards.append((x, y))
                else:
                    forwards.append(self.get(x, y))

            y = (r + x) + c
            if 0 <= y < len(self.matrix):
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
        if 0 <= r < len(self.matrix) and 0 <= c < len(self.matrix):
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
        if 0 <= r < len(self.matrix) and 0 <= c < len(self.matrix) and (force is True or self.get(r, c) == ' '):
            self.matrix[r][c] = value
            return True
        else:
            return False

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
        for _r in range(len(self.matrix)):
            if self.row(_r).count(' ') > 0:
                return False
        
        return True

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
        size = len(self.matrix)

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
