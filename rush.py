
# Tkinter zit standaard in python xy
import Tkinter

class Visualization:
    def __init__(self, width, height):
        #self.num_autos = num_autos
        self.max_dim = max(width, height)
        self.width = width
        self.height = height

        #draw canvas
        self.root = Tkinter.Tk()
        self.canvas = Tkinter.Canvas(self.root, width = 500, height = 500)
        self.canvas.pack()
        self.root.update()
       
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")

        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.canvas.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.canvas.create_line(x1, y1, x2, y2)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def done(self):
        mainloop()

a = Visualization(300,300)

######### 
# Maybe it is more convenient to have a class to make position objects
# so it is easier to get coordinates?
#########
class Position:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def get_position(self):
		return (self.x,self.y)
	def get_x(self):
		return self.x
	def get_y(self):
		return self.y
	def get_up(self):
		if self.y > 0
			return Position(self.x,self.y-1)
	def get_down(self):
		if self.y > 0
			return Position(self.x,self.y+1)
	def get_left(self):
		if self.x > 0
			return Position(self.x-1,self.y)
	def get_right(self):
		if self.x > 0
			return Position(self.x+1,self.y)
	def __eq__(self,other):
		return self.x == other.x and self.y == other.y
	def __ne__(self,other):
		return self.x != other.x or self.y != other.y
	def __repr__(self):
		return (self.x, self.y)

# p1 = Position(1,2)
# p2 = Position(2,2)

# print p1 == p1, p1 == p2, p2 != p2, p1 != p2



#########
# NOTE:
# de gamestates opslaan als dictionary is handig maar er ontstaan problemen
# wanneer de dicts in een set worden opgeslagen (sequentie van gamestates)
# waarschijnlijk moeten we een andere manier vinden om het op te slaan
# zodat de gamestates in een set kunnen worden opgeslagen...
#########
class Board:
	"""
	Represents a board with moveable car objects (auto) and an exit.
	"""
	def __init__(self, width, height, gamestate, empty_pos, exit_pos):
		"""
		Initializes the board with its width,height. The initial
		gamestate,exit and emptyfields are stored.
		width: integer
		height: integer
		gamestate: dictionary -> key; auto ,
			value; list of occupied positions as Position.
		empty_pos: set of Position objects on the board that are empty.

		"""
		self.width = width
		self.height = height
		self.gamestate = gamestate
		self.exit = exit_pos
		self.empty = empty_pos

	def check_moveability(self, auto):
		# returns an empty list when the car is immovable
		# otherwise returns all directions the car 
		# could move in in a list maximum -1 and +1
		moves = []

		if auto.get_direction() == 0:
			# can the car go forward or backward vertically:
			front_pos = gamestate[auto][0] # Position object
			end_pos = gamestate[auto][-1] # Position object
			up = front_pos.get_up()
			down = end_pos.get_down()
			
			if up != None:
				if self.is_empty(up):
					moves.append(-1)
			if down != None:
				if self.is_empty(up):
					moves.append(1)
		else:
			# can the car go forward or backward horizontally:
			front_pos = gamestate[auto][0] # Position object
			end_pos = gamestate[auto][-1] # Position object
			left = front_pos.get_left()
			right = end_pos.get_right()
			
			if up != None:
				if self.is_empty(left):
					moves.append(-1)
			if down != None:
				if self.is_empty(right):
					moves.append(1)

		return moves

	def move_car(self, auto, move):
		# moves car up/down (+1 or -1) in x or y, depending
		# on the direction.
		# move: integer -1 or 1
		# also changes the empty_pos set accordingly

		if auto.direction == 0:
			if move == 1:
				pos = gamestate[auto][-1]

	def save_gamestate(self):
		# TO DO:
		# Wat is handiger:
		# 1. Een heel bord kopieren en meegeven?
		# 2. Alleen de dictionary meegeven?
		return self.gamestate

	def is_empty(self, position):
		return position in empty

class Auto:
	# TO DO:
	# Misschien moeten we ze een id geven, zodat we ze beter uit elkaar kunnen halen.
	# Dat moeten we dan ook in de input verwerken? of gwn oo volgorde van 
	# alle natuurlijke getallen

    def __init__(self, width, height, color = None):
        self.width = width
        self.height = height
        self.color = color

        if self.width > self.height:
            self.direction = 1 # 1 = horizontal
        else:
            self.directon = 0 # 0 = vertical
        
        def get_direction(self):
            return self.direction



def load_game(gamefilename):
	# TO DO:
	# hier moet moet ook een set gemaakt worden met alle vlakken
	# elke keer als een veld word ingenomen door een wagen wordt 
	# deze uit de set verwijderd ---setnaam.remove((1,2))---
	# en uiteindelijk hou je een set over met lege velden die dan
	# mee wordt gegeven aan het board

	## ook posities moeten een Position object worden en in die set worden gezet.
	pass
