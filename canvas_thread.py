import threading
import board

class MoveThread(threading.Thread):
	def __init__(self, wid, x_from, y_from, x_to, y_to):
		threading.Thread.__init__(self)
		self.piece_wid = wid
		self.x_pos, self.y_pos = x_from, y_from
		self.x_from, self.y_from = x_from, y_from
		self.x_to, self.y_to = x_to, y_to
		self.dx, self.dy = (x_to - x_from) / 100, (y_to - y_from) / 100
	  
	def run(self):
		if self.can_move():
			self.x_pos, self.y_pos = self.x_pos + self.dx, self.y_pos + self.dy
			board.Board.canvas.move(self.piece_wid, self.dx * board.Board.square_size , self.dy * board.Board.square_size)
			board.Board.canvas.update()
			board.Board.canvas.after(2, self.run)
		else:
			board.Board.canvas.coords(self.piece_wid, board.Board.pad_x + ((self.x_to + 0.5) * board.Board.square_size), board.Board.pad_y + ((self.y_to + 0.5) * board.Board.square_size))
	  
	#can move for animation
	def can_move(self):
		if self.dx <= 0:
			x_can = self.x_to < self.x_pos 
		else:
			x_can = self.x_to > self.x_pos 
			
		if self.dy <= 0:
			y_can = self.y_to < self.y_pos 
		else:
			y_can = self.y_to > self.y_pos 
			
		return x_can or y_can