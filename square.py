import board
import pieces

class Square:
	def __init__(self, x, y, color, wid):
		self.x = x			#x_pos 0-7
		self.y = y			#y_pos 0-7
		self.color = color	#square color 'black'/'white'
		self.piece = None	#instance of piece class
		self.wid = wid		#canvas wid of square
	
	def create_piece(self, piece, piece_color, x, y, on_board):
		if piece == 'P':
			return pieces.Pawn(piece_color, x, y, on_board)
		elif piece == 'R':
			return pieces.Rook(piece_color, x, y, on_board)
		elif piece == 'k':
			return pieces.Knight(piece_color, x, y, on_board)
		elif piece == 'B':
			return pieces.Bishop(piece_color, x, y, on_board)
		elif piece == 'Q':
			return pieces.Queen(piece_color, x, y, on_board)
		else:
			return pieces.King(piece_color, x, y, on_board)
	
	@property
	def coords(self):
		return self.x, self.y
	
	def add_piece(self, piece, piece_color, on_board=0):#vyriesit pre ai
		self.piece = self.create_piece(piece, piece_color, self.x, self.y, on_board)
		
	#remove piece from grid and canvas
	def remove_piece(self, on_board=0):
		if not on_board:
			board.Board.canvas.delete(self.piece.wid)
		self.piece = None
		
	#return True when on this square is enemy piece
	def is_enemy(self, player_color):
		if not self.is_empty():
			return player_color != self.piece.color
		return False
		
	#return True when this square is empty
	def is_empty(self):
		return self.piece == None
		
	#returns True if the players piece is on the enemy's pawn rank
	def on_opponents_pawn_rank(self, color):
		y = self.y
		
		if (color == 'w' and y == 1) or (color == 'b' and y == 6):
			return True
		return False
		
	#returns True if the players piece is on his pawn rank
	def on_my_pawn_rank(self, color):
		y = self.y
		
		if (color == 'b' and y == 1) or (color == 'w' and y == 6):
			return True
		return False
	
	