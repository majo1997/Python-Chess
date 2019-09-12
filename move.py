class Move:
	#special - 0,1,2,3,4
	#0 - None
	#1 - en passant
	#2 - pawn change
	#3 - castling (king side)
	#4 - castling (queen side)
	
	def __init__(self, from_x, from_y, to_x, to_y, special):
		self._from_x = from_x
		self._from_y = from_y
		self._to_x = to_x
		self._to_y = to_y
		self._special = special
		
	def enpassant_last(self, fromy, fromx, toy, tox):
		return fromx == self._from_x and fromy == self._from_y and tox == self._to_x and toy == self._to_y
		
	@property
	def coords_to(self):
		return self._to_x ,	self._to_y
		
	@property
	def coords(self):
		return self._from_x ,self._from_y ,self._to_x ,	self._to_y
		
	@property
	def special(self):
		return self._special
		
	@property
	def length(self):
		return (self._to_x - self._from_x, self._to_y - self._from_y)
		
	def long_jump(self, x, y, color):
		dir = {'w': -1, 'b': 1}[color]
		
		if self._to_y == y and self._to_x == x and self._from_y == y + (2 * dir) and self._from_x == x:
			return True
		return False
		

class Moves(list):
	#__contains__ return whether move(x, y) is in moves as destination coords
	def __contains__(self, move):
		to_moves = [m.coords_to for m in self]
		return move in to_moves
		
	#returns the move with the square destination coords
	def get_move(self, square_coords):
		x, y = square_coords
		for m in self:
			if m._to_x == x and m._to_y == y:
				return m
				
	def no_castling(self):
		for i in reversed(range(len(self))):
			if self[i].special in (4, 5):
				self.remove(m)
		