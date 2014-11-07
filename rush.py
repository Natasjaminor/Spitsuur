
import rushvisua

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
		if other == None:
			return False
		return self.x == other.x and self.y == other.y
	def __ne__(self,other):
		if other == None:
			return True
		return not(self.x == other.x and self.y == other.y)
	def __repr__(self):
		return  str((self.x,self.y))
	def __hash__(self):
		return hash((self.x,self.y))





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
	  # otherwise returns all top-left positions 
	  # the car could take (first position)
	  # in a list
		new_top_pos_list = []

		if auto.get_direction() == "v":
			# can the car go forward or backward vertically:
			front_pos = self.gamestate[auto][0] # Position object
			end_pos = self.gamestate[auto][-1] # Position object
			up = front_pos.get_up()
			down = end_pos.get_down()
		   
			if up != None:
				if self.is_empty(up):
					new_top_pos_list.append(up)
			if down != None:
			    if self.is_empty(down):
					new_top_pos_list.append(front_pos.get_down())
		else:
			# can the car go forward or backward horizontally:
			front_pos = self.gamestate[auto][0] # Position object
			end_pos = self.gamestate[auto][-1] # Position object
			left = front_pos.get_left()
			right = end_pos.get_right()
		    
			if left != None:
			    if self.is_empty(left):
			        new_top_pos_list.append(left)
			if right != None:
			    if self.is_empty(right):
			        new_top_pos_list.append(front_pos.get_right())

		return new_top_pos_list
	
	def get_new_positions(self, auto, top_pos):
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

	def move_auto(self, auto, top_pos):
		# Changes position of car in gamestate dictionary to the pos_list given
		# and the difference will be used to update all empty fields?
		# top_pos : new top-left position for the car
		old_pos = list(self.gamestate[auto]) #makes a copy
		new_pos = self.get_new_positions(auto,top_pos)
		self.gamestate[auto] = new_pos
		for i in old_pos:
			if not (i in new_pos):
				self.empty.append(i)
				break
		for i in new_pos:
			if not (i in old_pos):
				self.empty.remove(i)
				break

	def get_gamestate(self):
		# TO DO:
		# Wat is handiger:
		# 1. Een heel bord kopieren en meegeven?
		# 2. Alleen de dictionary meegeven?
		return self.gamestate

	def is_empty(self, pos):
		# Returns True if a position is empty, False if it is taken.
		return pos in self.empty

class Auto:
     # TO DO:
     # Misschien moeten we ze een id geven, zodat we ze beter uit elkaar kunnen halen.
     # Dat moeten we dan ook in de input verwerken? of gwn oo volgorde van 
     # alle natuurlijke getallen
    def __init__(self, direction, length, color = None, ID = None):
        self.length = length
        self.direction = direction
        self.color = color
        self.ID = ID
    def get_direction(self):
        return self.direction
    def get_color(self):
    	return self.color
    def get_length(self):
    	return self.length
    def __eq__(self, other):
    	return self.ID == other.ID
    def __ne__(self,other):
    	return self.ID != other.ID
    def __hash__(self):
        return hash(self.ID)
    def __repr__(self):
    	return "AUTO-ID("+ str(self.ID)+ ")"

######## misschien kan assign er uit want komt in Board()...
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

	car_id = 0

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
				exit_pos = Position(x,exit,board_dimensions)
	        else:
	        	color = None
	        car_id += 1
	        car = Auto(direction,length,color,car_id)
	        taken_positions = assign_positions(car,top_pos)
	        
	        gamestate[car] = taken_positions
	        for i in taken_positions:
	        	empty_pos.remove(i)
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

def visualize(game):
    cars_pos = load_yas(game)
    width= int(cars_pos[0])
    height = int(cars_pos[0])
    cars_loc = cars_pos[1]
    empty = cars_pos[2]
    exit = cars_pos[3]
    app = rushvisua.BoardVisualization(width, height)
    #print exit
    print cars_loc.values()
    for values in cars_loc.values():
        
        if len(values) > 2:
            begin_values = values[0]
            middle_values = values[1]
            end_values = values[2]
        else:
            begin_values = values[0]
            end_values = values[1]
        x1 = begin_values.get_x()
        y1 = begin_values.get_y()
        x2 = end_values.get_x()
        y2 = end_values.get_y()
        app._draw_cars(x1,y1,x2,y2)
    app.done()


if __name__ == "__main__":

        
	game = "game_new.txt"
	dim, gs, em, ex = load_yas(game)

	BB = Board(dim, gs, em, ex)
	# for i in gs:
	# 	print i, " : ", gs[i]
	# 	print gs[i][-1] in ep
	
	print "gs before: ", gs
	print "empty before: ", em
	print len(em)
	moved_dict = {}
	m1 ={}
	m2 = {}
	c = 1
	for i in BB.gamestate:
		car = i
		m1[car] = c
		m2[car] = c+1
		moves = BB.check_moveability(car)
		BB.move_auto(car,moves[0])
		
	print "gs after: ", gs
	print "em after: ", BB.empty
	print len(BB.empty)
	
	# hier komt true uit terwijl dit niet true is
	# hoe kunnen we dit fixen?
	print "Are the gamestates the same?: ", gs == BB.get_gamestate() 
	print m1 == m2





