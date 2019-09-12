import tkinter
import board
from tkinter import messagebox
import tkinter.ttk as ttk
import grid
import os
import time
import pieces
#import pickle
import webbrowser

class Game:
	def __init__(self):
		self.master = tkinter.Tk()
		
		self.master.iconbitmap(default='resources/images/icon.ico')
		self.master.title('Chess')
		
		menu = tkinter.Menu(self.master)
		self.master.config(menu=menu)
		
		###########################################################################
		
		game = tkinter.Menu(menu, tearoff=False)
		game.add_command(label='New game...', command=lambda: New_game(self.master))
		game.add_command(label='Load game...', command=lambda: Load_game(self.master))
		game.add_command(label='Save game...', command=lambda: Save_game(self.master))
		
		game.add_separator()
		
		game.add_command(label='Exit', command=self.master.destroy)#ak dame exit tak sa a neulozilo sa tak sa opytat ci ulozit
		
		menu.add_cascade(label='Game', menu=game)
		
		###########################################################################
		
		edit = tkinter.Menu(menu, tearoff=False)
		edit.add_command(label='About...', command=lambda: About(self.master))
		
		menu.add_cascade(label='Help', menu=edit)
		
		###########################################################################
		
		square_size = 50
		pad_x, pad_y = 10, 10
		
		canv_width = 8 * square_size + 2 * pad_x
		canv_height = 8 * square_size + 2 * pad_y
		
		self.canvas = tkinter.Canvas(self.master, width=canv_width, height=canv_height)
		self.canvas.pack()

		#start new game
		board.canvas = self.canvas
		Game.canvas_grid = board.Board()
		
		tkinter.mainloop()
		
class New_game:
	def __init__(self, master):
		self.master = tkinter.Toplevel(master)
		self.master.geometry('300x200')
		self.master.resizable(False, False)
		#self.master = master
		#master.skovat/odkryt()
		
		self.master.iconbitmap(default='resources/images/icon.ico')
		self.master.title('Chess - New Game')
		
		self.frame_top = tkinter.Frame(self.master)
		self.frame_top.grid(row=0, column=0, columnspan=2)
		
		self.frame_left = tkinter.Frame(self.master, relief=tkinter.SUNKEN, borderwidth=1)#mozeme pridat height a width
		self.frame_left.grid(row=1, column=0, padx=0, pady=10)
		
		self.frame_right = tkinter.Frame(self.master, relief=tkinter.SUNKEN, borderwidth=1)
		self.frame_right.grid(row=1, column=1, pady=10)
		
		self.frame_mid = tkinter.Frame(self.master, relief=tkinter.SUNKEN, borderwidth=1)
		self.frame_mid.grid(row=2, column=0, columnspan=2)#, sticky='we')
		#self.master.grid_columnconfigure(0, weight=1)
		
		self.frame_bottom = tkinter.Frame(self.master)
		self.frame_bottom.grid(row=3, column=0, columnspan=2, pady=10)
		
		###############################################################
		
		self.label0 = tkinter.Label(self.frame_top, text='Settings:')
		self.label0.grid(row=0, column=0, padx=120, pady=5)
		
		###############################################################
		
		self.label1 = tkinter.Label(self.frame_left, text='Game type:')
		self.label1.grid(row=0, column=0, columnspan=2)

		#1-player, 2-player
		#ak 2-player ostatok sa nenastavuje(obtiaznost a farba)
		#ak sa nastavi 2-player co by sa nemalo nastavit po otvoreni okna(malo by sa nastavit 1-player by default) tak sa disablne prava strana tie nastavenia
		
		game_modes = [
        ('1-player', 1),
        ('2-player', 2),
		]
		
		self.type = tkinter.StringVar()
		self.type.set(1)
		
		self.radio_b1 = []
		
		for i, (text, mode) in enumerate(game_modes):
			self.radiob = tkinter.Radiobutton(self.frame_left, text=text, variable=self.type, value=mode, indicatoron=0)
			if i == 0:
				self.radiob.config(command=self.show)
			else:
				self.radiob.config(command=self.hide)
			self.radiob.grid(row=1, column=i, padx=5, pady=5)
			self.radio_b1.append(self.radiob)

		###############################################################
		#white, black
		self.label2 = tkinter.Label(self.frame_right, text='Play as:')
		self.label2.grid(row=0, column=0, columnspan=2)
		
		player_colors = [
        ('White', 1),#############mozno by mohlo byt 'w'/'b' nie 1/2
        ('Black', 2),
		]
		
		self.player_color = tkinter.StringVar()
		self.player_color.set(1)
		
		imgs = [
		tkinter.PhotoImage(file='resources/images/w_pawn-icon.png'),
		tkinter.PhotoImage(file='resources/images/b_pawn-icon.png'),
		]
		
		self.radio_b2 = []
		
		for i, (text, mode) in enumerate(player_colors):
			self.b = tkinter.Radiobutton(self.frame_right, text=text, variable=self.player_color, value=mode, indicatoron=0, image=imgs[i], height=20, width=20)#, state=tkinter.ACTIVE)
			self.b.image = imgs[i]

			self.b.grid(row=1, column=i, padx=5)
			self.radio_b2.append(self.b)
		
		##############################################################

		self.label3 = tkinter.Label(self.frame_mid, text='Choose difficulty:')
		self.label3.grid(row=0, column=0, padx=20, pady=5)
		
		difficulty_levels = [
        ('1', 1),
        ('2', 2),
		('3', 3),
		('4', 4),
		('5', 5),
		]
		
		self.difficulty_level = tkinter.StringVar()
		self.difficulty_level.set(3)
		
		self.radio_b3 = []
		
		for i, (text, mode) in enumerate(difficulty_levels):
			self.b = tkinter.Radiobutton(self.frame_mid, text=text, variable=self.difficulty_level, value=mode, indicatoron=0)
			self.b.grid(row=0, column=i+1, padx=5)
			
			self.radio_b3.append(self.b)
		#############################################################
		
		self.play_btn = tkinter.Button(self.frame_bottom, text='Play', command=self.create_new_game)
		self.play_btn.grid(row=0, column=1, pady=5)
		
	def create_new_game(self):
		#treba overit ci su vsetky hodnoty vyplnene(tie co maju byt) a getnut hodnoty
		number_of_players = int(self.type.get())
		player_color = int(self.player_color.get())
		ai_level = int(self.difficulty_level.get())
		
		if number_of_players == 2:
			game_type = 2
		elif number_of_players == 1 and player_color == 2:
			game_type = 1
		elif number_of_players == 1 and player_color == 1:
			game_type = 0
		
		Game.canvas_grid = board.Board(type=game_type, level=ai_level)
		self.master.destroy()
		
		
	def show(self):
		for radio_b in self.radio_b2:
			radio_b.config(state=tkinter.ACTIVE)
			
		for radio_b in self.radio_b3:
			radio_b.config(state=tkinter.ACTIVE)		
		
	def hide(self):
		for radio_b in self.radio_b2:
			radio_b.config(state=tkinter.DISABLED)
			
		for radio_b in self.radio_b3:
			radio_b.config(state=tkinter.DISABLED)
		
class Load_game:
	def __init__(self, master):
		#sort by name, date default=date
		#print(['.'.join(file.split('.')[0:len(file.split('.'))-1]) for file in os.listdir(os.getcwd() + '\\resources\\saved_games')])
		list_a = [('.'.join(file.split('.')[0:len(file.split('.'))-1]), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(os.getcwd() + '\\resources\\saved_games\\'+file)))) for file in os.listdir(os.getcwd() + '\\resources\\saved_games')]
		
		#list_a.sort(key=lambda x: x[1], reverse=True)
		
		
		self.master = tkinter.Toplevel(master)
		self.master.geometry('300x280')

		self.master.iconbitmap(default='resources/images/icon.ico')
		self.master.title('Chess - Load Game')
		
		#selectmode - moznost vybrat len 1 z viacerych
		##self.lb = tkinter.Listbox(self.master, exportselection=0, selectmode=tkinter.SINGLE)
		##self.lb.grid(row=0, column=0)
		#self.frame1 = tkinter.Frame(self.master)
		#self.frame1.pack()
		
		#statbuf = os.stat(os.getcwd() + '\\resources\\saved_games\\' + item)
		lb_header = ['name', 'date']
		#lb_list = [
		#('John', 'Smith') ,
		#('Larry', 'Black') ,
		#('Walter', 'White') ,
		#('Fred', 'Becker') 
		#]

		self.tree = ttk.Treeview(self.master,columns=lb_header, show='headings')
		self.tree.grid(row=0, column=0, padx=20, pady=5, columnspan=2)
		#self.tree.pack(side='left')

		for col in lb_header:
			self.tree.heading(col, text=col.title(), command=lambda x=col : self.sort(x))
			self.tree.column(col, width=120)
					
		for item in list_a:
			self.tree.insert('', 'end', values=item)
			
		self.vsb = ttk.Scrollbar(self.master, orient='vertical', command=self.tree.yview)
		self.vsb.place(x=260+1, y=5, height=227)
		#self.vsb.grid(row=0, column=1)
		#self.vsb.pack(side='right', fill='y')
		self.tree.configure(yscrollcommand=self.vsb.set)
		#nech to nepodciarkuje oznacene hodnoty treba spravit
		#for item in list_a:
		#	self.lb.insert(tkinter.END, item)
			
		self.button = tkinter.Button(self.master, text='Load', command=self.load_game)
		self.button.grid(row=1, column = 0)
		
		self.button_del = tkinter.Button(self.master, text='Delete', command=self.delete)
		self.button_del.grid(row=1, column = 1)
		
		#self.label = tkinter.Label(self.frame, text='Save game as:')
		#self.label.grid(row=0, column=0)
		
		#self.tree.bind('<<TreeviewSelect>>', self.on_select)
		#self.selected = []

	#def on_select(self, event):
	#	self.selected = event.widget.selection()	
	
	def sort(self, col):
		
		list_a = [('.'.join(file.split('.')[0:len(file.split('.'))-1]), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(os.getcwd() + '\\resources\\saved_games\\'+file)))) for file in os.listdir(os.getcwd() + '\\resources\\saved_games')]
		self.tree.delete(*self.tree.get_children())
		
		if col == 'date':
			list_a.sort(key=lambda x: x[1], reverse=True)
		else:
			list_a.sort(key=lambda x: x[0])
			
		for item in list_a:
			self.tree.insert('', 'end', values=item)
	
	def load_game(self):
		file_name = self.tree.item(self.tree.focus())['values'][0] + '.txt'
		#print(self.tree.item(self.tree.focus())['values'][0])
		Game.canvas_grid = board.Board(file_name=file_name)
		self.master.destroy()

		
	def delete(self):
		file_name = self.tree.item(self.tree.focus())['values'][0] + '.txt'
		
		question_ans = messagebox.askquestion('Load Game', 'Are you sure to delete this saved game?', icon = 'warning', parent=self.master)
				
		#overwrite saved game
		if question_ans == 'yes':
			os.remove(os.getcwd() + '\\resources\\saved_games\\' + file_name)
			self.tree.delete(*self.tree.get_children())
			list_a = [('.'.join(file.split('.')[0:len(file.split('.'))-1]), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(os.getcwd() + '\\resources\\saved_games\\'+file)))) for file in os.listdir(os.getcwd() + '\\resources\\saved_games')]
			for item in list_a:
				self.tree.insert('', 'end', values=item)
			
			
		
class Save_game:
	def __init__(self, master):
	
		self.master = tkinter.Toplevel(master)
		self.master.geometry('280x70')

		self.master.iconbitmap(default='resources/images/icon.ico')
		self.master.title('Chess - Save Game')
		
		self.frame_top = tkinter.Frame(self.master)
		self.frame_top.grid(row=0, column=0, pady=5)
		
		self.frame_bottom = tkinter.Frame(self.master)
		self.frame_bottom.grid(row=1, column=0, columnspan=2)
		self.master.grid_columnconfigure(0, weight=1)
		
		self.label = tkinter.Label(self.frame_top, text='Save game as:')
		self.label.grid(row=0, column=0, padx=15)
		
		self.entered_name = tkinter.StringVar()
		self.entry = tkinter.Entry(self.frame_top, textvariable=self.entered_name)
		self.entry.grid(row=0, column=1, padx=15)
		
		self.button = tkinter.Button(self.frame_bottom, text='Save', command=self.save_game)
		self.button.grid(row=0, column=1, padx=200 )
		
		self.path = 'resources\\saved_games'
		
	def save_game(self):
		file_name = self.entered_name.get()
		
		if file_name == '':
			messagebox.showerror('Error', 'No name has been entered.', parent=self.master)
		else:
			#returns names of saved games
			saved_games = ['.'.join(file.split('.')[0:len(file.split('.'))-1]) for file in os.listdir(os.path.join(os.getcwd(), self.path))]

			#if file_name exists
			if file_name in saved_games:
				#return value 'yes'/'no'
				question_ans = messagebox.askquestion('Save game', 'The entered name already exists. Do you want to overwrite it?', icon = 'warning', parent=self.master)
				
				#overwrite saved game
				if question_ans == 'yes':		
					self.write_to_file(os.path.join(self.path, file_name + '.txt'))
					self.master.destroy()
						
			#if file_name doesn't exist
			else:
				self.write_to_file(os.path.join(self.path, file_name + '.txt'))
				self.master.destroy()
	
	def write_to_file(self, file_name):
		self.board = Game.canvas_grid
		grid = self.board.grid
	
		with open(file_name, 'w') as file:
			print(grid.player_turn, file=file)
			
			if grid.check['w']:
				print('w', file=file)
			elif grid.check['b']:
				print('b', file=file)
			else:
				print(file=file)
			
			if grid.last_move:
				coords = ' '.join(map(str, grid.last_move.coords))
				print(coords, grid.last_move.special, file=file)
			else:
				print(file=file)
				
			print(self.board.type, file=file)
			
			if self.board.ai:
				print((self.board.ai.level + 1), file=file)
			else:
				print(file=file)
			
			for y in range(8):
				for x in range(8):
					if grid[y][x].piece:
						
						if isinstance(grid[y][x].piece, pieces.Pawn):
							piece = 'P'
						elif isinstance(grid[y][x].piece, pieces.Rook):
							piece = 'R'
						elif isinstance(grid[y][x].piece, pieces.Knight):
							piece = 'k'
						elif isinstance(grid[y][x].piece, pieces.Bishop):
							piece = 'B'
						elif isinstance(grid[y][x].piece, pieces.Queen):
							piece = 'Q'
						elif isinstance(grid[y][x].piece, pieces.King):
							piece = 'K'
							
						print(grid[y][x].piece.color, file=file, end='')
					else:
						piece = '0'
					print(piece, file=file, end='')
						
				print(file=file)
		
class About:
	def __init__(self, master):
		self.master = tkinter.Toplevel(master)
		self.master.geometry('300x100')
		
		self.master.iconbitmap(default='resources/images/icon.ico')
		self.master.title('Chess - About')
		
		self.frame = tkinter.Frame(self.master)
		self.frame.pack(fill='both', expand=True)
		self.frame.pack()

		self.msg = tkinter.Message(self.frame, text='Ročníkový projekt 1', width=300)
		self.msg.pack()
		
		self.msg = tkinter.Message(self.frame, text='Autor projektu: Mário Hlavačka', width=300)
		self.msg.pack()
		
		link1 = tkinter.Label(self.frame, text='Stránka projektu', fg='blue', cursor='hand2')
		link1.pack()
		link1.bind('<Button-1>', lambda e: self.open('http://www.st.fmph.uniba.sk/~hlavacka12/roc_projekt'))
		
	def open(self, url):
		webbrowser.open_new(url)
		
class Choose_piece:
	def __init__(self, master, color):
		self.master = tkinter.Toplevel(master)
		self.master.geometry('300x280')
		
		self.master.iconbitmap(default='resources/images/icon.ico')
		self.master.title('Chess - Select piece')
		
		self.frame = tkinter.Frame(self.master)
		self.frame.pack()
		
		self.label = tkinter.Label(self.frame, text='Choose piece to change:\n', font='Arial 15')
		self.label.grid(row=0, column=0, columnspan=2)
		
		self.choosen_piece = tkinter.StringVar()
		
		# initialize and choose queen when window closed
		
		self.choosen_piece.set('Q')

		img_queen = tkinter.PhotoImage(file='resources/images/'+ color +'_queen.png')
		img_bishop = tkinter.PhotoImage(file='resources/images/'+ color +'_bishop.png')
		img_knight = tkinter.PhotoImage(file='resources/images/'+ color +'_knight.png')
		img_rook = tkinter.PhotoImage(file='resources/images/'+ color +'_rook.png')
		
		imgs = []
		imgs.append(img_queen)
		imgs.append(img_bishop)
		imgs.append(img_knight)
		imgs.append(img_rook)
		
		pieces = [
        ('Queen', 'Q'),
        ('Bishop', 'B'),
		('Knight', 'k'),
		('Rook', 'R'),
		]
		
		for i, (text, mode) in enumerate(pieces, 1):
			self.lab = tkinter.Label(self.frame, text=text, font='Arial 15')
			self.lab.grid(row=i, column=0, columnspan=1)
		
			self.b = tkinter.Radiobutton(self.frame, text=text, variable=self.choosen_piece, value=mode, indicatoron=0, image=imgs[i-1], command=self.master.destroy)
			self.b.image = imgs[i-1]

			self.b.grid(row=i, column=1, columnspan=1)

	def choose(self):
		self.master.deiconify()
		self.master.wait_window()
		
		return self.choosen_piece.get()

class Game_over:
	def __init__(self, master, color=None):
		self.master = tkinter.Toplevel(master)
		self.master.geometry('250x50')
		
		self.frame = tkinter.Frame(self.master)
		self.frame.pack()
		
		if not color:
			self.master.iconbitmap(default='resources/images/icon.ico')
			self.master.title('Chess - Draw')
			
			self.label = tkinter.Label(self.frame, text='Stale mate!')
			self.label.grid(row=0, column=0)
			self.label.config(font=('Arial', 20))
		else:
			self.master.iconbitmap(default='resources/images/icon.ico')
			self.master.title('Chess - Win')
			
			self.label = tkinter.Label(self.frame, text={'w': 'Black ','b': 'White '}[color] + 'player wins!')
			self.label.grid(row=0, column=0)
			self.label.config(font=('Arial', 20))
		