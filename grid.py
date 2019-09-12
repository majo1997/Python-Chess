import board
import pieces
import move
import copy
import canvas_thread

class Grid(list):
	def __init__(self, player_turn, onboard_pieces, kings, check, last_move, list=False):
		for i in range(8):
			self.append([0 for i in range(8)])
			
		self.player_turn = player_turn
		self.onboard_pieces = onboard_pieces
		self.check = check #True - ten ktory sa oznaci 
		self.last_move = last_move
		self.kings = kings
		
		if list:
			for i in range(len(list)):
				for j in range(len(list[i])):
					self[i][j] = list[i][j]
			
	def is_in_check(self, x, y, castling=None):
		moves = move.Moves()
		
		for x_p, y_p in self.onboard_pieces[self.opponent_color()]:
			if not castling:
				moves_no_castling = self[y_p][x_p].piece.valid_moves((x_p, y_p), self)#toto
			else:
				if isinstance(self[y_p][x_p].piece, pieces.King):
					moves_no_castling = self[y_p][x_p].piece.valid_moves((x_p, y_p), self, 1)
				else:
					moves_no_castling = self[y_p][x_p].piece.valid_moves((x_p, y_p), self)
				
			for m in moves_no_castling:
				if m.special in (0, 1, 2):
					moves.append(m)
		
		return (x, y) in moves
		
	def delete_from_onboard(self, x, y, color):
		self.onboard_pieces[color].remove((x, y))
		
	def add_to_onboard(self, x, y, color):
		self.onboard_pieces[color].append((x, y))
		
	def move_onboard(self, x_from, y_from, x_to, y_to, color):
		self.delete_from_onboard(x_from, y_from, color)
		self.add_to_onboard(x_to, y_to, color)
	
	def move_piece(self, x_from, y_from, x_to, y_to, on_board=0):
		self.move_onboard(x_from, y_from, x_to, y_to, self[y_from][x_from].piece.color)
		if not on_board:
			# Create new threads
			thread1 = canvas_thread.MoveThread(self[y_from][x_from].piece.wid, x_from, y_from, x_to, y_to)

			# Start new Threads
			thread1.start()

			#thread1.join()
			
		self[y_to][x_to].piece = self[y_from][x_from].piece
		self[y_from][x_from].piece = None
		
		
	def opponent_color(self):
		return {'w': 'b', 'b': 'w'}[self.player_turn]
		
	#return True if the coordinates are on board else return False
	def on_board(self, x, y):
		return 0 <= x < 8 and 0 <= y < 8	
		
	def get_copy(self):
		return copy.deepcopy(self)
		
		