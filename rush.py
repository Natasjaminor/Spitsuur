
# import rushvisua

######### 
# Maybe it is more convenient to have a class to make position objects
# so it is easier to get coordinates?
#########
class Position:
     def __init__(self,x,y,dimensions):
          self.x = x
          self.y = y
          self.dimensions = dimensions
     def get_position(self):
          return (self.x,self.y)
     def get_x(self):
          return self.x
     def get_y(self):
          return self.y
     def get_up(self):
        if self.y > 1:
            return Position(self.x,self.y-1,self.dimensions)
     def get_down(self):
          if self.y < self.dimensions:
           return Position(self.x,self.y+1,self.dimensions)
     def get_left(self):
          if self.x > 1 :
           return Position(self.x-1,self.y,self.dimensions)
     def get_right(self):
        if self.x < self.dimensions:
            return Position(self.x+1,self.y,self.dimensions)
     def change_position(self, pos):
     	self.x = pos.get_x()
     	self.y = pos.get_y()
     def __eq__(self,other):
          return self.x == other.x and self.y == other.y
     def __ne__(self,other):
          return self.x != other.x or self.y != other.y
     def __repr__(self):
          return  str((self.x,self.y))


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
	def __init__(self, dimensions, gamestate, empty_pos, exit_pos):
	  """
	  Initializes the board with its dimensions. The initial
	  gamestate,exit and emptyfields are stored.
	  dimensions: integer
	  gamestate: dictionary -> key; auto ,
	       value; list of occupied positions as Position.
	  empty_pos: set of Position objects on the board that are empty.

	  """
	  self.dimensions = dimensions
	  self.gamestate = gamestate
	  self.exit = exit_pos
	  self.empty = empty_pos

	def check_moveability(self, auto):
	  # returns an empty list when the car is immovable
	  # otherwise returns all directions the car 
	  # could move in in a list
		moves = []

		if auto.get_direction() == 0:
			# can the car go forward or backward vertically:
			front_pos = gamestate[auto][0] # Position object
			end_pos = gamestate[auto][-1] # Position object
			up = front_pos.get_up()
			down = end_pos.get_down()
		   
			if up != None:
				if self.is_empty(up):
					moves.append("up")
			if down != None:
			    if self.is_empty(up):
					moves.append("down")
		else:
			# can the car go forward or backward horizontally:
			front_pos = gamestate[auto][0] # Position object
			end_pos = gamestate[auto][-1] # Position object
			left = front_pos.get_left()
			right = end_pos.get_right()
		   
			if up != None:
			    if self.is_empty(left):
			        moves.append("left")
			if down != None:
			    if self.is_empty(right):
			        moves.append("right")

		return moves

	def move_car(self, auto, pos_list):
		# Changes position of car in gamestate dictionary to the pos_list given
		# and the difference will be used to update all empty fields?
	  	pass

	def save_gamestate(self):
		# TO DO:
		# Wat is handiger:
		# 1. Een heel bord kopieren en meegeven?
		# 2. Alleen de dictionary meegeven?
		return self.gamestate

	def is_empty(self, position):
		# Returns True if a position is empty, False if it is taken.
		return position in empty

class Auto:
     # TO DO:
     # Misschien moeten we ze een id geven, zodat we ze beter uit elkaar kunnen halen.
     # Dat moeten we dan ook in de input verwerken? of gwn oo volgorde van 
     # alle natuurlijke getallen
    def __init__(self, direction, length, color = None):
        self.length = length
        self.direction = direction
        self.color = color
    def get_direction(self):
        return self.direction
    def get_color(self):
    	return self.color
    def get_length(self):
    	return self.length

def assign_positions(auto, top_pos):
	# retuns a list of position which are taken by the car
	# starting from the top left position the car stands on
	pos_list = [top_pos]
	if auto.get_direction() == "h":
		for i in range(auto.length-1):
			p = pos_list[i]
			pos_list.append(p.get_right())
	else:
		for i in range(auto.length-1):
			p = pos_list[i]
			pos_list.append(p.get_down())

	return pos_list

def generate_all_positions(dimensions):
	all_pos = []
	for i in range(1,dimensions+1):
		for j in range(1,dimensions+1):
			all_pos.append(Position(i,j,dimensions))
	return all_pos


def load_yas(gamefilename):
	inputFile = open(gamefilename)
	gamestate = {}

	for line in inputFile:
	    line_elements = line.strip()
	    line_elements = line_elements.split(" ")
	    if line_elements[0] == '*' or line_elements[0] == '':
	    	continue
	    elif line_elements[0] == '#':
	    	board_dimensions = int(line_elements[1])
	    	empty_pos = generate_all_positions(board_dimensions)
	    else:
	    	direction = line_elements[0] 
	        length = int(line_elements[1]) 
	        x = int(line_elements[2]) 
	        y = int(line_elements[3])
	        top_pos = Position(x,y,board_dimensions)
	        if line_elements[-1] == 'r':
				color = 'red'
				if board_dimensions%2 == 0:
					exit = board_dimensions/2
				else:
					exit = board_dimensions/2 +1
				exit_pos = Position(x,board_dimensions,board_dimensions)
	        else:
	        	color = None
	        car = Auto(direction,length,color)
	        taken_positions = assign_positions(car,top_pos)
	        
	        gamestate[car] = taken_positions
	        for i in taken_positions:
	        	empty_pos.remove(i)
	print len(empty_pos)
	return board_dimensions, gamestate, empty_pos, exit_pos

def load_game(gamefilename):
    
     # TO DO:
     # hier moet moet ook een set gemaakt worden met alle vlakken
     # elke keer als een veld word ingenomen door een wagen wordt 
     # deze uit de set verwijderd ---setnaam.remove((1,2))---
     # en uiteindelijk hou je een set over met lege velden die dan
     # mee wordt gegeven aan het board

     ## ook posities moeten een Position object worden en in die set worden gezet.

    inputFile = open(gamefilename)
    cars = []
    board = rushvisua.BoardVisualization(4,4)

    for line in inputFile:
        aline = line.strip()
        theline = aline.split(" ")

        width = int(theline[0]) 
        height = int(theline[1]) 
        x = int(theline[2]) 
        y = int(theline[3])
        color = theline[4]
        print width, height, x, y, color
        board._draw_cars(x,y,width,height, color)
    board.done()
        
    
game = "game_new.txt"
dim, gs, ep, ex = load_yas(game)
print ep
board_test = Board(dim, gs, ep, ex)
