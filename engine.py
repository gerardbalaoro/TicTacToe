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
        out = '-' * 55 + '\n'
        for x in range(3):
            for inner_x in range(3):
                for y in range(3):
                    out += '|   '
                    for inner_y in range(3):
                        if self.big[x][y] != ' ':
                            if inner_y == 0:
                                if inner_x == 1:
                                    out += ' '*5 + self.big[x][y] + ' '*5
                                else:
                                    out += ' '*11
                        else:
                            out += ' {} '.format(self.matrix[x][y][inner_x][inner_y])
                            if inner_y != 2:
                                out += '|'
                    out += '   '
                out += '|\n'
                for y in range(3):
                    if inner_x != 2:
                        if self.big[x][y] != ' ':
                            out += ('|' + ' '*17)
                        else:
                            out += ('|   ' + '-' * 11 + '   ')
                        if y == 2:
                            out += '|\n'
            out += '-' * 55 + '\n'
        print(out)

    def row(self, n, x=3, y=3):
        """
        Gets a single row from one of the inner boards or from the main summarized board
        
        Arguments:
            n {int} -- zero-based row number for the inner board
            x {int} -- zero-based row number for the main board
            y {int} -- zero-based column number for the main board
        
        Returns:
            tuple of the row
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
            tuple of the column
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
            if self.big[x][y] == ' ':
                self.big[x][y] = value
        else:
            if self.matrix[x][y][ix][iy] == ' ':
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
            A tuple containing who won and the line/s made, with the coordinates of the start of the line,
            '-' if there's a draw, or False otherwise. (The lines can either be 'v', 'h', 'd+', or 'd-',
            which represents the orientations vertical, horizontal, diagonal with positive slope, and
            diagonal with negative slope, respectively.)
        """
        lines = []

        if ix == 3 or iy == 3:
            value = self.big[x][y]

            if value != '-':
                if self.row(x).count(value) == 3:
                    lines.append(('h', x, 0))

                if self.column(y).count(value) == 3:
                    lines.append(('v', 0, y))

                if self.big[0][2] == value and self.big[1][1] == value and self.big[2][0] == value:
                    lines.append(('d+', 0, 2))
                if self.big[0][0] == value and self.big[1][1] == value and self.big[2][2] == value:
                    lines.append(('d-', 0, 0))

            if len(lines) > 0:
                return value, tuple(lines)
            else:
                space = 0
                for r in range(3):
                    space += self.big[r].count(' ')
                if space == 0:
                    return '-'
        else:
            value = self.matrix[x][y][ix][iy]

            if self.row(ix, x, y).count(value) == 3:
                lines.append(('h', x, y, ix, 0))

            if self.column(iy, x, y).count(value) == 3:
                lines.append(('v', x, y, 0, iy))

            if (self.matrix[x][y][0][2] == value and
                    self.matrix[x][y][1][1] == value and
                    self.matrix[x][y][2][0] == value):
                lines.append(('d+', x, y, 0, 2))
            if (self.matrix[x][y][0][0] == value and
                    self.matrix[x][y][1][1] == value and
                    self.matrix[x][y][2][2] == value):
                lines.append(('d-', x, y, 0, 0))

            if len(lines) > 0:
                self.set(value, x, y)
                return value, tuple(lines)
            else:
                space = 0
                for r in range(3):
                    space += self.matrix[x][y][r].count(' ')
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
        print('\n'.join(['|\t' + '\t|\t'.join([col for col in row]) + '\t|' for row in self.matrix]))

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

    def diagonals(self, r, c):
        """Get diagonal values intersecting (r, c) coodinates

        Parameters:
            r {int} -- a zero based row number
            c {int} -- a zero based column number

        Returns:
            dict -- forward and backward diagonal values
        """
        forwards = []
        backwards = []

        for x in range(len(self.matrix)):
            y = (x - r) + c
            if 0 <= y < len(self.matrix):
                forwards.append(self.get(x, y))

            y = (r + x) + c
            if 0 <= y < len(self.matrix):
                backwards.append(self.get(x, y))

        return {'forward': tuple(forwards), 'backward': tuple(backwards)}        

    def get(self, r, c):
        """Get cell value
        
        Parameters:
            r {int} -- zero-based row number
            c {int} -- zero-based column number
        
        Returns:
            mixed -- False if (r, c) is out-of-bounds else cell value
        """
        if 0 <= r < len(self.matrix) and 0 <= c < len(self.matrix):
            return self.matrix[r][c]
        else:
            False

    def set(self, value, r, c, force = False):
        """Set cell value
        
        Parameters:
            value {str} -- value to assign
            r {int} -- zero-based row number
            c {int} -- zero-based column number
            force {bool} -- overwrite value on non-empty cells
        
        Returns:
            bool
        """
        if 0 <= r < len(self.matrix) and 0 <= c < len(self.matrix) and (force == True or self.get(r, c) == ' '):
            self.matrix[r][c] = value
            return True
        else:
            return False

    def flip(self, r, c, d, force = False):
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
        

        if d in self.canflip(r, c) or force == True:
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
                return (r, c)

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
        """Check if (r, c) value existing at least there times in a row vertically, horizontally, or diagonally
        
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
            if len(''.join(self.row(_r)).strip()) < len(self.matrix):
                return False
        
        return True

    def win(self, x, y):
        """
        Check if there is a line that can no longer be flipped out of place.
        
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        
        Returns:
            True if there is, False if otherwise
        """
        lines = self.check(x, y)
        if lines is not False:
            for line in lines:
                orient, x, y = line[0], int(line[1]), int(line[2])
                if orient == 'v':
                    for c in range(3):
                        if self.canflip(x+c, y) is not False:
                            return False
                elif orient == 'v4':
                    for c in range(4):
                        if self.canflip(x+c, y) is not False:
                            return False
                elif orient == 'h':
                    for c in range(3):
                        if self.canflip(x, y+c) is not False:
                            return False
                elif orient == 'h4':
                    for c in range(4):
                        if self.canflip(x, y+c) is not False:
                            return False
                elif orient == 'd+':
                    for c in range(3):
                        if self.canflip(x+c, y-c) is not False:
                            return False
                elif orient == 'd4+':
                    for c in range(4):
                        if self.canflip(x+c, y-c) is not False:
                            return False
                elif orient == 'd-':
                    for c in range(3):
                        if self.canflip(x+c, y+c) is not False:
                            return False
                elif orient == 'd4-':
                    for c in range(4):
                        if self.canflip(x+c, y+c) is not False:
                            return False
                return True
