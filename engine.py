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
        """
        Get cell value based on (x, y) coordinates

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
        """Prints the board in the terminal"""

        print('\n{}\n'.format('-'*15).join(['|'.join([' {} '.format(self.get(x, y))
                                                      for y in range(4)])for x in range(4)]))

    def row(self, n):
        """
        Gets a single row from the board
        Parameters:
            n {int} -- a zero based row number
        Returns:
            {tuple} -- contains the elements of row n
        """
        return tuple(self.matrix[n])

    def column(self, n):
        """
        Gets a single column from the board
        
        Parameters:
            n {int} -- a zero based row number
        
        Returns:
            {tuple} -- contains the elements of column n
        """
        return tuple([row[n] for row in self.matrix])

    def get(self, x, y):
        """
        Get cell value based on (x, y) coordinates
        
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        
        Returns:
            {str} -- the cell value
        """
        return self.matrix[x][y]

    def set(self, value, x, y):
        """
        Sets cell value of based on (x, y) coordinates
        
        Parameters:
            value {str} -- either 'X', 'x', 'O', or 'o'
            x {int} -- zero-based row number
            y {int} -- zero-based column number

        Returns:
            game_over {str} --  the value of the piece if an unflippable line of 3 is formed
                or '-' if there is a draw
        """
        self.matrix[x][y] = value

        game_over = self.won(x, y)
        if game_over is not False:
            return game_over

    def flip(self, x, y, d):
        """
        Flips the opponent's piece in one of the 4 cardinal directions
        ('u', 'd', 'l', and 'r', for up, down, left, and right, respectively
        
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
            d {str} -- either 'up', 'down', 'left', or 'right'

        Returns:
            True if the piece can be flipped,
            False if the piece can't be flipped, or
            value {str} -- the value of the piece if it gets flipped into a line of 3
        """

        if d not in self.can_flip(x, y):
            return False
        
        value = self.get(x, y)
        if value == value.lower():
            value = value.upper()
        else:
            value = value.lower()

        r, c = x, y
        if d == 'u':
            self.set(' ', x, y)
            r -= 1
            self.set(value, r, c)
        elif d == 'd':
            self.set(' ', x, y)
            r += 1
            self.set(value, r, c)
        elif d == 'l':
            self.set(' ', x, y)
            c -= 1
            self.set(value, r, c)
        elif d == 'r':
            self.set(' ', x, y)
            c += 1
            self.set(value, x, y + 1)

        if len(self.check(r, c)) > 0:
            return value
        
        return True

    def can_flip(self, x, y):
        """
        Checks if the cell value can still be flipped
        
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        
        Returns:
            can_go {list} -- contains the directions the cell value can flip to
        """
        can_go = []

        if self.get(x, y) != ' ':
            if x > 0:
                if self.get(x - 1, y) == ' ':
                    can_go.append('u')

            if x < 3:
                if self.get(x + 1, y) == ' ':
                    can_go.append('d')

            if y > 0:
                if self.get(x, y - 1) == ' ':
                    can_go.append('l')

            if y < 3:
                if self.get(x, y + 1) == ' ':
                    can_go.append('r')

        return can_go

    def check(self, x, y):
        """
        Checks if there is a line of 3 of the same value vertically, horizontally, or diagonally
        
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        
        Returns:
            lines {tuple} -- contains the line/s made, with the coordinates of the start of the line, or False
            (The lines can either be 'v', 'h', 'd+', or 'd-', which represents the orientations
            vertical, horizontal, diagonal with positive slope, and diagonal with negative slope,
            respectively.
        """
        value = self.get(x, y)

        lines = []

        if value == ' ':
            return lines

        if value*3 in self.column(y):
            lines.append(('v', self.column(y).index(value), y))
        elif self.column(y).count(value) == 4:
            lines.append(('v4', 0, y))

        if value*3 in self.row(x):
            lines.append(('h', x, self.row(x).index(value)))
        elif self.row(x).count(value) == 4:
            lines.append(('h4', x, 0))

        d4 = True
        for i in range(4):
            if self.matrix[3 - i][i] != value:
                d4 = False
                break
        if d4:
            lines.append(('d4+', 0, 3))
        elif x > 1 and y < 2:
            for i in range(3):
                if self.get(x - 1, y + 1) != value:
                    break
                if i == 2:
                    lines.append(('d+', x - 2, y + 2))
        elif 0 < x < 3 and 0 < y < 3:
            for i in range(3):
                if self.get(x + 1 - i, y - 1 + i) != value:
                    break
                if i == 2:
                    lines.append(('d+', x - 1, y + 1))
        elif x < 2 and y > 1:
            for i in range(3):
                if self.get(x + i, y - i) != value:
                    break
                if i == 2:
                    lines.append(('d+', x, y))

        d4 = True
        for i in range(4):
            if self.get(i, i) != value:
                d4 = False
                break
        if d4:
            lines.append(('d4-', 0, 0))
        elif x < 2 and y < 2:
            for i in range(3):
                if self.get(x + i, y + i) != value:
                    break
                if i == 2:
                    lines.append(('d-', x, y))
        elif 0 < x < 3 and 0 < y < 3:
            for i in range(3):
                if self.get(x - 1 + i, y - 1 + i) != value:
                    break
                if i == 2:
                    lines.append(('d-', x - 1, y - 1))
        elif x > 1 and y > 1:
            for i in range(3):
                if self.get(x - i, y - i) != value:
                    break
                if i == 2:
                    lines.append(('d-', x - 2, y - 2))

        return lines

    def won(self, x, y):
        """
        Checks if there is a line that can no longer be flipped out of place.
        (a player has won)
        
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        
        Returns:
            value {str} -- the value that won or '-' if there is a draw, or
            False if otherwise
        """

        if ' ' not in ''.join([''.join(self.row(r)) for r in range(4)]):
            return '-'

        value = self.get(x, y)
        lines = self.check(x, y)

        if len(lines) > 0:
            for line in lines:
                d, x, y = line[0], int(line[1]), int(line[2])
                
                if d == 'v':
                    for i in range(3):
                        if len(self.can_flip(x + i, y)) > 0:
                            return False
                elif d == 'v4':
                    for i in range(4):
                        if len(self.can_flip(x + i, y)) > 0:
                            return False
                        
                elif d == 'h':
                    for i in range(3):
                        if len(self.can_flip(x, y + i)) > 0:
                            return False
                elif d == 'h4':
                    for i in range(4):
                        if len(self.can_flip(x, y + i)) > 0:
                            return False
                        
                elif d == 'd+':
                    for i in range(3):
                        if len(self.can_flip(x + i, y - i)) > 0:
                            return False
                elif d == 'd4+':
                    for i in range(4):
                        if len(self.can_flip(x + i, y - i)) > 0:
                            return False
            
                elif d == 'd-':
                    for i in range(3):
                        if len(self.can_flip(x + i, y + i)) > 0:
                            return False
                elif d == 'd4-':
                    for i in range(4):
                        if len(self.can_flip(x + i, y + i)) > 0:
                            return False
                    
                return value
