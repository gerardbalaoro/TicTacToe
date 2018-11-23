class Board:
	"""TicTacToe Board Class"""

	def __init__(self, size=3):
		"""Initialize board matrix
		
		Arguments:
			size {int} -- length of sides (default: {3})
		"""
		self.__matrix = []
		for row in range(size):
			self.__matrix.append([None for col in range(size)])

	def board(self):
		"""Create a copy of the current state of the board matrix

		Returns:
			list
		"""
		return self.__matrix.copy()

	def toString(self):
		return '\n'.join([
			'|\t' + '\t|\t'.join(['-' if col == None else col for col in row]) + '\t|' for row in self.__matrix
		])
	
	def size(self):
		"""Get board size
		
		Returns:
			int
		"""
		return len(self.__matrix)
		
	def row(self,n):
		"""Get single row
		
		Arguments:
			n {int} -- zero-based row number
		
		Returns:
			tuple
		"""
		return tuple(self.__matrix[n])

	def column(self,n):
		"""Get single row
		
		Arguments:
			n {int} -- zero-based column number
		
		Returns:
			tuple
		"""
		return tuple([row[n] for row in self.__matrix])
			
	def get(self, x, y):
		"""Get cell value based on (x, y) coordinates
		
		Arguments:
			x {int} -- zero-based row number
			y {int} -- zero-based column number
		
		Returns:
			mixed
		"""
		return self.__matrix[x][y]

	def set(self, value, x, y):
		"""Set cell value of based on (x, y) coordinates
		
		Arguments:
			x {int} -- zero-based row number
			y {int} -- zero-based column number
		"""
		if self.get(x, y) == None:
			self.__matrix[x][y] = value
		
	def check(self, value, x=None, y=None):
		"""Check if the value existed N times vertically,
		horizontally, or diagonally. N is the size of the matrix
		
		Arguments:
			x {int} -- zero-based row number
			y {int} -- zero-based column number
		"""
		if self.row(x).count(value) == self.size():
			return True
		
		if self.column(y).count(value) == self.size():
			return True

		if (x in (0, self.size()-1) and y in (0, self.size()-1)) or (x in range(1, self.size()-1) and y in range(1, self.size()-1)):
			if x == y:
				for c in range(self.size()):
					if self.get(c, c) != value:
						return False
			else:
				for c in range(self.size()):
					if self.get(c, self.size()-1-c):
						return False
			return True

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
