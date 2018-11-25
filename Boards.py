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
        """Prints the board in the terminal"""
        print('\n'.join(['|\t' + '\t|\t'.join([col for col in row]) + '\t|' for row in self.matrix]))

    def row(self, n):
        """
        Gets a single row from the board
        Parameters:
            n {int} -- a zero based row number
        Returns:
            the row in tuple form
        """
        return tuple(self.matrix[n])

    def column(self, n):
        """
        Gets a single column from the board
        Parameters:
            n {int} -- a zero based row number
        Returns:
            the column in tuple form
        """
        return tuple([row[n] for row in self.matrix])

    def get(self, x, y):
        """
        Get cell value based on (x, y) coordinates
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        Returns:
            the cell value
        """
        return self.matrix[x][y]

    def set(self, value, x, y):
        """
        Sets cell value of based on (x, y) coordinates
        Parameters:
            value {str} -- either 'X', 'x', 'O', or 'o'
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        """
        self.matrix[x][y] = value

    def flip(self, x, y, d):
        """
        Flips the opponent's piece in one of the 4 cardinal directions
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
            d {str} -- either 'up', 'down', 'left', or 'right'
        """
        if self.matrix[x][y] == self.matrix[x][y].lower():
            self.matrix[x][y] = self.matrix[x][y].upper()
        else:
            self.matrix[x][y] = self.matrix[x][y].lower()

        if d == 'up':
            self.matrix[x][y], self.matrix[x - 1][y] = ' ', self.matrix[x][y]
        elif d == 'down':
            self.matrix[x][y], self.matrix[x + 1][y] = ' ', self.matrix[x][y]
        elif d == 'left':
            self.matrix[x][y], self.matrix[x][y - 1] = ' ', self.matrix[x][y]
        elif d == 'right':
            self.matrix[x][y], self.matrix[x][y + 1] = ' ', self.matrix[x][y]

    def canflip(self, x, y):
        """
        Checks if the cell value can still be flipped
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        Returns:
            A tuple of the directions it can flip to or False
        """
        can_go = []

        if x > 0:
            if self.matrix[x - 1][y] == ' ':
                self.flip(x, y, 'up')
                if self.check(x - 1, y) is False:
                    can_go.append('up')
                self.flip(x - 1, y, 'down')
        if x < 3:
            if self.matrix[x + 1][y] == ' ':
                self.flip(x, y, 'down')
                if self.check(x + 1, y) is False:
                    can_go.append('down')
                self.flip(x + 1, y, 'up')
        if y > 0:
            if self.matrix[x][y - 1] == ' ':
                self.flip(x, y, 'left')
                if self.check(x, y - 1) is False:
                    can_go.append('left')
                self.flip(x, y - 1, 'right')
        if y < 3:
            if self.matrix[x][y + 1] == ' ':
                self.flip(x, y, 'right')
                if self.check(x, y + 1) is False:
                    can_go.append('right')
                self.flip(x, y + 1, 'left')

        if len(can_go) > 0:
            return tuple(can_go)
        else:
            return False

    def check(self, x, y):
        """
        Checks if there is a line of 3 of the same value vertically, horizontally, or diagonally
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        Returns:
            A tuple of the line/s made, with the coordinates of the start of the line, or False
            (The lines can either be 'v', 'h', 'd+', or 'd-', which represents the orientations
            vertical, horizontal, diagonal with positive slope, and diagonal with negative slope,
            respectively. Just in case the line is 4 cells long, the orientation will have an
            addition '4' added to its string)
        """
        value = self.matrix[x][y]

        if value == ' ':
            return False

        lines = []

        if self.column(y).count(value) == 3:
            lines.append(('v', self.column(y).index(value), y))
        elif self.column(y).count(value) == 4:
            lines.append(('v4', 0, y))

        if self.row(x).count(value) == 3:
            lines.append(('h', x, self.row(x).index(value)))
        elif self.row(x).count(value) == 4:
            lines.append(('h4', x, 0))

        d4 = True
        for c in range(4):
            if self.matrix[3 - c][c] != value:
                d4 = False
                break
        if d4:
            lines.append(('d4+', 0, 3))
        elif x > 1 and y < 2:
            for c in range(3):
                if self.matrix[x - c][y + c] != value:
                    break
                if c == 2:
                    lines.append(('d+', x - 2, y + 2))
        elif 0 < x < 3 and 0 < y < 3:
            for c in range(3):
                if self.matrix[x + 1 - c][y - 1 + c] != value:
                    break
                if c == 2:
                    lines.append(('d+', x - 1, y + 1))
        elif x < 2 and y > 1:
            for c in range(3):
                if self.matrix[x + c][y - c] != value:
                    break
                if c == 2:
                    lines.append(('d+', x, y))

        d4 = True
        for c in range(4):
            if self.matrix[c][c] != value:
                d4 = False
                break
        if d4:
            lines.append(('d4-', 0, 0))
        elif x < 2 and y < 2:
            for c in range(3):
                if self.matrix[x + c][y + c] != value:
                    break
                if c == 2:
                    lines.append(('d-', x, y))
        elif 0 < x < 3 and 0 < y < 3:
            for c in range(3):
                if self.matrix[x - 1 + c][y - 1 + c] != value:
                    break
                if c == 2:
                    lines.append(('d-', x - 1, y - 1))
        elif x > 1 and y > 1:
            for c in range(3):
                if self.matrix[x - c][y - c] != value:
                    break
                if c == 2:
                    lines.append(('d-', x - 2, y - 2))

        if len(lines) > 0:
            return lines
        return False

    def win(self, x, y):
        """
        Checks if there is a line that can no longer be flipped out of place.
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
