
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

class Board:
	"""
	Represents a board with moveable car objects (auto) and an exit.
	"""
	def __init__(self, width, height, gamestate, exit_pos):
		"""
		Initializes the board with its 
		"""
		self.width = width
		self.height = height
		self.gamestate = gamestate
		self.exit = exit_pos

	def check_moveability(self, auto):
		# returns an empty list when the car is immovable
		# otherwise returns all directions the car 
		# could move in in a list
		if auto.get_direction() == 0:
			# can the car go forward or backward vertically:
			up = gamestate[auto][0][1] -1
			if game


	def move_car(self, forward_or_backward):
		# moves car up/down (+1 or -1) in x or y, depending
		# on the direction.
		# forward_or_backward: integer -1 or 1
		pass
	
	def save_gamestate(self):
		# returns a gamestate dict
		pass

class Auto:
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
# hier moet moet ook een set gemaakt worden met alle vlakken
# elke keer als een veld word ingenomen door een wagen wordt 
# deze uit de set verwijderd ---setnaam.remove((1,2))---
# en uiteindelijk hou je een set over met lege velden die dan
# mee wordt gegeven aan het board





