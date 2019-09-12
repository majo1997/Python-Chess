import AI
import grid
import gui
import square
import move
import pieces

class Board:
	canvas = None				#reference to canvas
	pad_x, pad_y = 10, 10		#padding size
	square_size = 50			#square size
	
	#Y - riadok 0-7
	#X - stlpec 0-7

	def __init__(self, file_name='new_game.txt', type=0, player_turn='w', level=3, check={ 'w': False, 'b': False }, last_move=None):
		#----------initialize basic attributes----------
		
		Board.canvas = canvas
		Board.canvas.bind('<ButtonPress>', self.klik)
		
		if file_name == 'new_game.txt':
			file_name = 'resources/new_game/' + file_name
		else:
			file_name = 'resources/saved_games/' + file_name
		
		with open(file_name, 'r') as file:
			player_turn = file.readline().strip()
			
			check_file = file.readline().strip()
			if check_file != '':
				check[check_file] = True
				
			last_move_file = file.readline().strip().split()
			
			if last_move_file:

				move_c = tuple(map(int, last_move_file))
				last_move = move.Move(*move_c)
				
			if not file_name == 'resources/new_game/new_game.txt':
				type = int(file.readline().strip())
			else:
				file.readline()
			
			if not file_name == 'resources/new_game/new_game.txt':
				level = int(file.readline().strip())
			else:
				file.readline()
				
			
			self.type = type		#game type(0 - white, 1 - black, 2 - 2 players)
			
			self.selected_square = tuple()	#clicked square coordinates(x, y) if seleceted or tuple() when not
			self.possible_moves = list()		#list of possible moves
			
			self.grid = grid.Grid(player_turn, {'w':[], 'b':[]}, {'w': tuple(), 'b': tuple()}, check, last_move)
				
			
			if type != 2:
				ai_color = 'w' if (type == 1) else 'b'
				self.ai = AI.AI(level, ai_color, self)
			else:
				self.ai = None
				

		#----------creating board squares----------
		
			for y in range(8):
				
				for x in range(8):
					color = 'white' if (x + y) % 2 == 0 else 'black'
					
					piece = None
					piece_color = None
					
					#corner1, corner2 - coordinates of the opposite corners for created square
					corner1 = (Board.pad_x + x * Board.square_size, Board.pad_y + y * Board.square_size)
					corner2 = (Board.pad_x + (x + 1) * Board.square_size, Board.pad_y + (y + 1) * Board.square_size)
					
					wid = self.canvas.create_rectangle(corner1, corner2, fill=color)
					
					self.grid[y][x] = square.Square(x, y, color, wid)
		
		#----------adding pieces from file----------
		
			for y in range(8):
				for x in range(8):
					piece = file.read(1)
					
					if piece == '\n':
						piece = file.read(1)
						
					if piece in 'bw':
						piece_color = piece
						piece = file.read(1)
						
					if piece == '0':
						continue
						
					self.grid[y][x].add_piece(piece, piece_color)
					self.grid.onboard_pieces[piece_color].append((x, y))
					
					if isinstance(self.grid[y][x].piece, pieces.King):
						self.grid.kings[piece_color] = (x, y)
		
		if self.grid.check['w']:
			coords = self.grid.kings['w']
			self.fill_square_red(coords)
		elif self.grid.check['b']:
			coords = self.grid.kings['b']
			self.fill_square_red(coords)
		
		if type == 1 and self.grid.player_turn == 'w':
			self.ai.best_move(self.grid, self.grid.player_turn)
					
			self.next_turn()
			if self.grid.is_in_check(*self.grid.kings[self.grid.player_turn]):
				self.grid.check[self.grid.player_turn] = True
				self.fill_square_red(self.grid.kings[self.grid.player_turn])
			if not self.can_move() and not self.grid.check[self.grid.player_turn]:
				gui.Game_over(self.canvas)
			if self.grid.check[self.grid.player_turn] and not self.can_get_from_check():
				gui.Game_over(self.canvas, self.grid.player_turn)
			
	
					
	#change turn state
	def next_turn(self):
		self.grid.player_turn = {'w': 'b', 'b': 'w'}[self.grid.player_turn]

	#return True if there is players(with color) piece on square with coords(x, y)
	def is_players_piece(self, color, x, y):
		#if there is a piece
		if self.grid[y][x].piece:
			return color == self.grid[y][x].piece.color
		return False
		
	def is_selected_square(self, x, y):
		sel_x, sel_y = self.selected_square
		return sel_x == x and sel_y == y
		
	def fill_square_yellow(self, square):
		color = self.grid.player_turn

		if isinstance(square, tuple):
			x, y = square
			
			if (self.grid.check[color] and not isinstance(self.grid[y][x].piece, pieces.King)) or (not self.grid.check[color]):
				self.canvas.itemconfig(self.grid[y][x].wid, fill='yellow')

		elif isinstance(square, move.Moves):
			for m in square:
				x, y = m.coords_to
				self.canvas.itemconfig(self.grid[y][x].wid, fill='yellow')

		self.canvas.update()

	def fill_square_red(self, square):
		x, y = square
		
		self.canvas.itemconfig(self.grid[y][x].wid, fill='red')
		self.canvas.update()

		
	def unfill_square(self, square):
		color = self.grid.player_turn
		
		if isinstance(square, tuple):
			x, y = square
		
		if isinstance(square, tuple) and ((not self.grid.check[color] and isinstance(self.grid[y][x].piece, pieces.King)) or (not isinstance(self.grid[y][x].piece, pieces.King))):
			x, y = square

			color = self.grid[y][x].color
			self.canvas.itemconfig(self.grid[y][x].wid, fill=color)
		elif isinstance(square, move.Moves):
			for m in square:
				x, y = m.coords_to
				color = self.grid[y][x].color
				self.canvas.itemconfig(self.grid[y][x].wid, fill=color)
		self.canvas.update()
				
	def do_selected_move(self, move, move_on_board=0, grid=None, ai_move=0):
		
		temp_grid = self.grid
		if grid:
			self.grid = grid
		
		tag = move.special
		x_from, y_from, x_to, y_to = move.coords
		
		if not move_on_board:
			if not ai_move:
				sel_x, sel_y = self.selected_square
			else:
				sel_x, sel_y = x_from, y_from
		else:
			sel_x, sel_y = x_from, y_from
			
			
		if isinstance(self.grid[sel_y][sel_x].piece, pieces.King):
			self.grid.kings[self.grid.player_turn] = x_to, y_to
		
		if tag == 0:
			if not self.grid[y_to][x_to].is_empty():
				self.grid[y_to][x_to].remove_piece(move_on_board)
				self.grid.delete_from_onboard(x_to, y_to, self.grid.opponent_color())

			self.grid.move_piece(x_from, y_from, x_to, y_to, move_on_board)
			
		elif tag == 1:
			en_pass_x = self.grid.last_move._to_x
			
			self.grid.move_piece(x_from, y_from, x_to, y_to, move_on_board)
			self.grid[y_from][x_to].remove_piece(move_on_board)
			self.grid.delete_from_onboard(x_to, y_from, self.grid.opponent_color())
			
		elif tag == 2:
			if not move_on_board and not ai_move:
				chosen_piece = gui.Choose_piece(self.canvas, self.grid.player_turn).choose()
			else:
				chosen_piece = 'Q'
			
			if not self.grid[y_to][x_to].is_empty():
				self.grid[y_to][x_to].remove_piece(move_on_board)
				self.grid.delete_from_onboard(x_to, y_to, self.grid.opponent_color())
			
			self.grid[y_from][x_from].remove_piece(move_on_board)
			self.grid.delete_from_onboard(x_from, y_from, self.grid.player_turn)
			self.grid[y_to][x_to].add_piece(chosen_piece, self.grid.player_turn, move_on_board)
			self.grid.add_to_onboard(x_to, y_to, self.grid.player_turn)
			
		elif tag == 3:
			self.grid.move_piece(x_from, y_from, x_to, y_to, move_on_board)
			self.grid.move_piece(x_from + 3, y_from, x_to - 1, y_to, move_on_board)
			
			self.grid[y_to][x_to].piece.moved = True
			self.grid[y_to][x_to - 1].piece.moved = True	
			
		elif tag == 4:
			self.grid.move_piece(x_from, y_from, x_to, y_to, move_on_board)
			self.grid.move_piece(x_from - 4, y_from, x_to + 1, y_to, move_on_board)
			
			self.grid[y_to][x_to].piece.moved = True
			self.grid[y_to][x_to + 1].piece.moved = True

		if grid:
			self.grid = temp_grid
		
	def remove_in_check_moves(self, moves, grid=None):
		if not grid:
			my_grid = self.grid
		else:
			my_grid = grid

		valid_moves = move.Moves()
		for m in moves:
			self.grid = my_grid.get_copy()
			self.do_selected_move(m, 1)
			
			x_k, y_k = self.grid.kings[self.grid.player_turn]
			if not self.grid.is_in_check(x_k, y_k):
				valid_moves.append(m)
				
		self.grid = my_grid

		
		return valid_moves
		
	#if player has some possible moves
	def can_move(self):
		color = self.grid.player_turn
		for x_p, y_p in self.grid.onboard_pieces[color]:
			moves = self.grid[y_p][x_p].piece.valid_moves((x_p, y_p), self.grid)
			moves = self.remove_in_check_moves(moves)
			
			if moves:
				return True
				
		return False
		
	def can_get_from_check(self):
		my_grid = self.grid

		color = self.grid.player_turn
		for x_p, y_p in self.grid.onboard_pieces[color]:
			moves = self.grid[y_p][x_p].piece.valid_moves((x_p, y_p), self.grid)
			moves = self.remove_in_check_moves(moves)
			
			for m in moves:
				self.grid = my_grid.get_copy()
				self.do_selected_move(m, 1)
				
				if not self.grid.is_in_check(*self.grid.kings[color]):
					self.grid = my_grid
					return True
				
		self.grid = my_grid
		
		return False
	
	def klik(self, event):
		x, y = (event.x - Board.pad_x) // Board.square_size, (event.y - Board.pad_y) // Board.square_size
		if self.grid.on_board(x, y):
		
			#----------if the player on turn, click on square with his piece and square has't been selected yet----------
			if not self.selected_square and self.is_players_piece(self.grid.player_turn, x, y):
				#choose selected square and get possible moves
				self.selected_square = (x, y)

				self.possible_moves = self.grid[y][x].piece.valid_moves((x, y), self.grid)#moze vratit uz moves priamo
				self.possible_moves = self.remove_in_check_moves(self.possible_moves)
				
				#fill the squares
				self.fill_square_yellow(self.selected_square)
				self.fill_square_yellow(self.possible_moves)
				
			#----------if the player click on the same piece again----------
			elif self.selected_square and self.is_selected_square(x, y):
				#unfill the squares
				self.unfill_square(self.selected_square)
				self.unfill_square(self.possible_moves)
				
				#set them to default
				self.selected_square = tuple()
				self.possible_moves = list()
				
			#----------if the player want to make a move----------
			elif self.selected_square and (x, y) in self.possible_moves:
				
				self.unfill_square(self.selected_square)
				self.unfill_square(self.possible_moves)
				
				x_king, y_king = self.grid.kings[self.grid.player_turn]
				
				self.grid.last_move = self.possible_moves.get_move((x, y))
				self.do_selected_move(self.grid.last_move)

				
				self.grid.check[self.grid.player_turn] = self.grid.is_in_check(*self.grid.kings[self.grid.player_turn])
				if not self.grid.check[self.grid.player_turn]:
					self.unfill_square((x_king, y_king))

					
				self.selected_square = tuple()
				self.possible_moves = list()
				
				if self.type == 2:
						
					self.next_turn()
					if self.grid.is_in_check(*self.grid.kings[self.grid.player_turn]):
						self.grid.check[self.grid.player_turn] = True

						self.fill_square_red(self.grid.kings[self.grid.player_turn])
						
					if not self.can_move() and not self.grid.check[self.grid.player_turn]:
						gui.Game_over(self.canvas)
					if self.grid.check[self.grid.player_turn] and not self.can_get_from_check():
						gui.Game_over(self.canvas, self.grid.player_turn)
						
				else:
					self.next_turn()
					
					
					if self.grid.is_in_check(*self.grid.kings[self.grid.player_turn]):
						self.grid.check[self.grid.player_turn] = True
						
						self.fill_square_red(self.grid.kings[self.grid.player_turn])
					if not self.can_move() and not self.grid.check[self.grid.player_turn]:
						gui.Game_over(self.canvas)
					if self.grid.check[self.grid.player_turn] and not self.can_get_from_check():
						gui.Game_over(self.canvas, self.grid.player_turn)

					x_king, y_king = self.grid.kings[self.grid.player_turn]
					
					self.grid.last_move = self.ai.best_move(self.grid, self.grid.player_turn)
					
					self.grid.check[self.grid.player_turn] = self.grid.is_in_check(*self.grid.kings[self.grid.player_turn])
					if not self.grid.check[self.grid.player_turn]:
						self.unfill_square((x_king, y_king))					
						
					self.next_turn()
					
					if self.grid.is_in_check(*self.grid.kings[self.grid.player_turn]):
						self.grid.check[self.grid.player_turn] = True

						self.fill_square_red(self.grid.kings[self.grid.player_turn])
					if not self.can_move() and not self.grid.check[self.grid.player_turn]:

						gui.Game_over(self.canvas)
					if self.grid.check[self.grid.player_turn] and not self.can_get_from_check():

						gui.Game_over(self.canvas, self.grid.player_turn)
				
			
			#----------if the player select another piece----------
			elif self.selected_square and self.is_players_piece(self.grid.player_turn, x, y):
				#unfill squares
				self.unfill_square(self.selected_square)
				self.unfill_square(self.possible_moves)
				
				
				self.selected_square = (x, y)
				self.fill_square_yellow(self.selected_square)
				
				self.possible_moves = self.grid[y][x].piece.valid_moves((x, y), self.grid)#moze vratit uz moves priamo
				self.possible_moves = self.remove_in_check_moves(self.possible_moves)

				self.fill_square_yellow(self.possible_moves)
				
