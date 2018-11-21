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
