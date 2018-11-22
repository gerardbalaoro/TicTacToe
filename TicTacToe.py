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
    """TicTacToe Flip Game Mode"""

    def __init__(self):
        """Initializes the 4x4 board"""

        self.matrix = []
        for row in range(4):
            self.matrix.append([' ' for _ in range(4)])

    def board(self):
        """
        Create a copy of the current state of the board matrix
        Returns:
             The board matrix in list form
        """
        return self.matrix.copy()

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
            self.matrix[x][y], self.matrix[x-1][y] = ' ', self.matrix[x][y]
        elif d == 'down':
            self.matrix[x][y], self.matrix[x+1][y] = ' ', self.matrix[x][y]
        elif d == 'left':
            self.matrix[x][y], self.matrix[x][y-1] = ' ', self.matrix[x][y]
        else:
            self.matrix[x][y], self.matrix[x][y+1] = ' ', self.matrix[x][y]

    def canflip(self, x, y):
        """
        Checks if the cell value can still be flipped
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        Returns:
            A tuple of the directions it can flip to or False
        """
        can = []

        if x > 0:
            if self.matrix[x-1][y] == ' ':
                can.append('up')
        if x < 3:
            if self.matrix[x+1][y] == ' ':
                can.append('down')
        if y > 0:
            if self.matrix[x][y-1] == ' ':
                can.append('left')
        if y < 3:
            if self.matrix[x][y+1] == ' ':
                can.append('right')

        if len(can) > 0:
            return tuple(can)
        else:
            return False

    def check(self, x, y):
        """
        Checks if there is a line of 3 of the same value vertically, horizontally, or diagonally
        Parameters:
            x {int} -- zero-based row number
            y {int} -- zero-based column number
        Returns:
            A tuple of the line/s made or False
        """
        value = self.matrix[x][y]

        """INCOMPLETE"""
