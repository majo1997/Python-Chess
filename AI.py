import pieces
import grid

class AI():
	def __init__(self, level, ai_color, board):
		self.level = level - 1
		self.ai_color = ai_color
		self.color_values = {'w': 1, 'b': -1}
		self.board = board
	
		#eval matrices for each piece for improved evaluation

		#king
		self.pos_king = [
		[-3, -4, -4, -5, -5, -4, -4, -3],
		[-3, -4, -4, -5, -5, -4, -4, -3],
		[-3, -4, -4, -5, -5, -4, -4, -3],
		[-3, -4, -4, -5, -5, -4, -4, -3],
		[-2, -3, -3, -4, -4, -3, -3, -2],
		[-1, -2, -2, -2, -2, -2, -2, -1],
		[2, 2, 0, 0, 0, 0, 2, 2],
		[2, 3, 1, 0, 0, 1, 3, 2],
		]

		#queen
		self.pos_queen = [
		[-2, -1, -1, -0.5, -0.5, -1, -1, -2],
		[-1, 0, 0, 0, 0, 0, 0, -1],
		[-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
		[-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
		[0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
		[-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
		[-1, 0, 0.5, 0, 0, 0, 0, -1],
		[-2, -1, -1, -0.5, -0.5, -1, -1, -2],
		]

		#rook
		self.pos_rook = [
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0.5, 1, 1, 1, 1, 1, 1, 0.5],
		[-0.5, 0, 0, 0, 0, 0, 0, -0.5],
		[-0.5, 0, 0, 0, 0, 0, 0, -0.5],
		[-0.5, 0, 0, 0, 0, 0, 0, -0.5],
		[-0.5, 0, 0, 0, 0, 0, 0, -0.5],
		[-0.5, 0, 0, 0, 0, 0, 0, -0.5],
		[0, 0, 0, 0.5, 0.5, 0, 0, 0],
		]

		#bishop
		self.pos_bishop = [
		[-2, -1, -1, -1, -1, -1, -1, -1, -2],
		[-1, 0, 0, 0, 0, 0, 0, -1],
		[-1, 0, 0.5, 1, 1, 0.5, 0, -1],
		[-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
		[-1, 0, 1, 1, 1, 1, 0, -1],
		[-1, 1, 1, 1, 1, 1, 1, -1],
		[-1, 0.5, 0, 0, 0, 0, 0.5, -1],
		[-2, -1, -1, -1, -1, -1, -1, -2],
		]

		#knight
		self.pos_knight = [
		[-5, -4, -3, -3, -3, -3, -4, -5],
		[-4, -2, 0, 0, 0, 0, -2, -4],
		[-3, 0, 1, 1.5, 1.5, 1, 0, -3],
		[-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
		[-3, 0, 1.5, 2, 2, 1.5, 0, -3],
		[-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
		[-4, -2, 0, 0.5, 0.5, 0, -2, -4],
		[-5, -4, -3, -3, -3, -3, -4, -5],
		]

		#pawn
		self.pos_pawn = [
		[0, 0, 0, 0, 0, 0, 0, 0],
		[5, 5, 5, 5, 5, 5, 5, 5],
		[1, 1, 2, 3, 3, 2, 1, 1],
		[0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
		[0, 0, 0, 2, 2, 0, 0, 0],
		[0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
		[0.5, 1, 1, -2, -2, 1, 1, 0.5],
		[0, 0, 0, 0, 0, 0, 0, 0],
		]
		
	def best_move(self, grid, turn):

		move = AInode(self, self.board, grid.get_copy(), self.level)
		
		self.board.do_selected_move(move.best, ai_move=1)
		
		return move.best
		
	def evaluate(self, grid):
		value = 0
		
		#piece values
		#10-pawn
		#30-knight
		#30-bishop
		#50-rook
		#90-queen
		#900-king
		
		for l in grid.onboard_pieces.values():
			for x, y in l:
				x_pos, y_pos = (x, y) if grid[y][x].piece.color == 'w' else (7 - x, 7 - y)
				
				if isinstance(grid[y][x].piece, pieces.Pawn):
					value += (10 * self.pos_pawn[y_pos][x_pos] * self.color_values[grid[y][x].piece.color])
				elif isinstance(grid[y][x].piece, pieces.King):
					value += (900 * self.pos_king[y_pos][x_pos] * self.color_values[grid[y][x].piece.color])
				elif isinstance(grid[y][x].piece, pieces.Queen):
					value += (90 * self.pos_queen[y_pos][x_pos] * self.color_values[grid[y][x].piece.color])
				elif isinstance(grid[y][x].piece, pieces.Bishop):
					value += (30 * self.pos_bishop[y_pos][x_pos] * self.color_values[grid[y][x].piece.color])
				elif isinstance(grid[y][x].piece, pieces.Knight):
					value += (30 * self.pos_knight[y_pos][x_pos] * self.color_values[grid[y][x].piece.color])
				elif isinstance(grid[y][x].piece, pieces.Rook):
					value += (50 * self.pos_rook[y_pos][x_pos] * self.color_values[grid[y][x].piece.color])
	
		return value
		
class AInode:
	def __init__(self, ai, board, grid, depth=0, move=None):
		temp = board.grid
		self.grid = grid
		self.move = move
		self.children = []
		
		if depth > 0:
			for coords in self.grid.onboard_pieces[self.grid.player_turn]:
				x, y = coords
				moves = self.grid[y][x].piece.valid_moves(coords, grid)
				moves = board.remove_in_check_moves(moves, grid)
				
				for m in moves:
					new_grid = self.grid.get_copy()
					
					board.do_selected_move(m, 1, new_grid)

					new_grid.player_turn = self.grid.opponent_color()
					self.children.append(AInode(ai, board, new_grid, depth - 1, m))#tu je chyba
					
		#if the node is not leaf get value from children
		if self.children:
			self.val = self.min_max()
			#if the node is root
			if not move:
				for child in self.children:
					if self.val == child.val:
						self.best = child.move
		else:
			self.val = ai.evaluate(self.grid)
		
			
		board.grid = temp
	
	#return min/max value depending on player color
	def min_max(self):
		color = self.grid.player_turn
		
		children_values = []
		
		for n in self.children:
			children_values.append(n.val)
		
		if color == 'w':
			return max(children_values)
		else:
			return min(children_values)
		