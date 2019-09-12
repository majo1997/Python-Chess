import tkinter
import board # for the canvas and the position, where to create a piece
import move

class Piece:
	def __init__(self, color, pic, x, y, on_board):	#x, y - stlpec a riadok
		self.color = color
		
		label = tkinter.Label()
		label.image = pic	# keep a reference
		
		coords = board.Board.pad_x + x * board.Board.square_size + board.Board.square_size / 2, board.Board.pad_y + y * board.Board.square_size + board.Board.square_size / 2
		
		if not on_board:
			self.wid = board.Board.canvas.create_image(coords, image=pic)
			
		board.Board.canvas.update()

#special moves for King - castling(king side, queen side)
class King(Piece):
	def __init__(self, color, x, y, on_board=0):
		pic = tkinter.PhotoImage(file='resources/images/' + color + '_king.png')
		self.moved = False
			
		super().__init__(color, pic, x, y, on_board)

	def valid_moves(self, square_coords, grid, castling=None):
		moves = move.Moves()
		x, y = square_coords
		
		for dx, dy in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
			if grid.on_board(x + dx, y + dy) and (grid[y + dy][x + dx].is_empty() or grid[y + dy][x + dx].is_enemy(self.color)):
				moves.append(move.Move(x, y, x + dx, y + dy, 0))

		if not castling and not self.moved:
			if self.possible_queen_castling(square_coords, grid):
				moves.append(move.Move(x, y, x - 2, y, 4))
				
			if self.possible_king_castling(square_coords, grid):
				moves.append(move.Move(x, y, x + 2, y, 3))

		return moves
	#The king and the chosen rook are on the player's first rank.[3]
	#Neither the king nor the chosen rook has previously moved.
	#There are no pieces between the king and the chosen rook.
	#The king is not currently in check.
	#The king does not pass through a square that is attacked by an enemy piece.[4]
	#The king does not end up in check. (True of any legal move.)
	
	def possible_queen_castling(self, square_coords, grid):
		x, y = square_coords
		
		if not grid.on_board(x - 4, y):
			return False
		
		empty_squares = grid[y][x - 3].is_empty() and grid[y][x - 2].is_empty() and grid[y][x - 1].is_empty()
		not_in_check_squares = not (grid.is_in_check(x - 3, y, 1) or grid.is_in_check(x - 2, y, 1) or grid.is_in_check(x - 1, y, 1) or grid.is_in_check(x, y, 1))
		
		#king not moved - rook on left side - rook not moved - the 3 squares are empty - the 3 squares and the king actual square is not in check
		return (not self.moved) and isinstance(grid[y][x - 4].piece, Rook) and (not grid[y][x - 4].piece.moved) and empty_squares and not_in_check_squares
		
	def possible_king_castling(self, square_coords, grid):
		x, y = square_coords
		
		if not grid.on_board(x + 3, y):
			return False
			
		empty_squares = grid[y][x + 2].is_empty() and grid[y][x + 1].is_empty()
		
		not_in_check_squares = not (grid.is_in_check(x + 2, y, 1) or grid.is_in_check(x + 1, y, 1) or grid.is_in_check(x, y, 1))
		
		return (not self.moved) and isinstance(grid[y][x + 3].piece, Rook) and (not grid[y][x + 3].piece.moved) and empty_squares and not_in_check_squares
	
class Queen(Piece):
	def __init__(self, color, x, y, on_board=0):
		pic = tkinter.PhotoImage(file='resources/images/' + color + '_queen.png')

		super().__init__(color, pic, x, y, on_board)

	def valid_moves(self, square_coords, grid):
		moves = move.Moves()
		x, y = square_coords

		for x_dir, y_dir in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
			dx, dy = x_dir, y_dir
			while grid.on_board(x + dx, y + dy):
				if grid[y + dy][x + dx].is_empty() or grid[y + dy][x + dx].is_enemy(self.color):
					moves.append(move.Move(x, y, x + dx, y + dy, 0))
					if grid[y + dy][x + dx].is_enemy(self.color):
						break
					dx, dy = dx + x_dir, dy + y_dir
				else:
					break
					
		return moves
		
		
class Bishop(Piece):
	def __init__(self, color, x, y, on_board=0):
		pic = tkinter.PhotoImage(file='resources/images/' + color + '_bishop.png')
		
		super().__init__(color, pic, x, y, on_board)
		
	def valid_moves(self, square_coords, grid):
		moves = move.Moves()
		x, y = square_coords
				
		for x_dir, y_dir in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
			dx, dy = x_dir, y_dir
			while grid.on_board(x + dx, y + dy):
				if grid[y + dy][x + dx].is_empty() or grid[y + dy][x + dx].is_enemy(self.color):
					moves.append(move.Move(x, y, x + dx, y + dy, 0))
					if grid[y + dy][x + dx].is_enemy(self.color):
						break
					dx, dy = dx + x_dir, dy + y_dir
				else:
					break
					
		return moves
		
class Knight(Piece):
	def __init__(self, color, x, y, on_board=0):
		pic = tkinter.PhotoImage(file='resources/images/' + color + '_knight.png')
		
		super().__init__(color, pic, x, y, on_board)

	def valid_moves(self, square_coords, grid):
		moves = move.Moves()
		x, y = square_coords
		
		for dx, dy in [(1, 2), (2, 1), (-1, 2), (2, -1), (-2, 1), (1, -2), (-2, -1), (-1, -2)]:
			if grid.on_board(x + dx, y + dy) and (grid[y + dy][x + dx].is_empty() or grid[y + dy][x + dx].is_enemy(self.color)):
				moves.append(move.Move(x, y, x + dx, y + dy, 0))
					
		return moves
		
class Rook(Piece):
	def __init__(self, color, x, y, on_board=0):
		pic = tkinter.PhotoImage(file='resources/images/' + color + '_rook.png')
		self.moved = False
		
		super().__init__(color, pic, x, y, on_board)

	def valid_moves(self, square_coords, grid):
		moves = move.Moves()
		x, y = square_coords
		
		for x_dir, y_dir in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
			dx, dy = x_dir, y_dir
			while grid.on_board(x + dx, y + dy):
				if grid[y + dy][x + dx].is_empty() or grid[y + dy][x + dx].is_enemy(self.color):
					moves.append(move.Move(x, y, x + dx, y + dy, 0))
					if grid[y + dy][x + dx].is_enemy(self.color):
						break
					dx, dy = dx + x_dir, dy + y_dir
				else:
					break
					
		return moves

class Pawn(Piece):
	def __init__(self, color, x, y, on_board=0):
	
		pic = tkinter.PhotoImage(file='resources/images/' + color + '_pawn.png')
			
		super().__init__(color, pic, x, y, on_board)
		
	def valid_moves(self, square_coords, grid):
		moves = move.Moves()
		x, y = square_coords
		dir = {'w': -1, 'b': 1}[self.color] #direction for player color
		special = 0
		
		#if the piece is on the opponents pawn rank
		if grid[y][x].on_opponents_pawn_rank(self.color):
			special = 2
			
		#normal move
		if grid.on_board(x, y + dir) and grid[y + dir][x].is_empty():
			moves.append(move.Move(x, y, x, y + dir, special))
				
		#to the side on enemy piece
		for dx in [-1, 1]:
			if grid.on_board(x + dx, y + dir) and grid[y + dir][x + dx].is_enemy(self.color):
				moves.append(move.Move(x, y, x + dx, y + dir, special))
		
		#long jump
		if grid.on_board(x, y + (2 * dir)) and grid[y][x].on_my_pawn_rank(self.color) and grid[y + dir][x].is_empty() and grid[y + (2 * dir)][x].is_empty():
			moves.append(move.Move(x, y, x, y + (2 * dir), 0))
		
		#en passant
		dx_en_passant = self.moved_pawn_longjump(grid, x, y)
		if dx_en_passant:
			moves.append(move.Move(x, y, x + dx_en_passant, y + dir, 1))
		
		return moves
		
		
	#returns dx for possible enpassant move, 0 when not possible
	def moved_pawn_longjump(self, grid, x, y):
		color = self.color
		for dx in [-1, 1]:
			if grid.on_board(x + dx, y) and grid[y][x + dx].is_enemy(color) and isinstance(grid[y][x + dx].piece, Pawn) and grid.last_move and grid.last_move.long_jump(x + dx, y, color):
				return dx
		return 0
	
	