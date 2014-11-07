
# Dit is een kopie van rush, 
# alleen moeten hier posities als tuples geimplementeerd worden


# import rushvisua


#########
# NOTE:
# de gamestates opslaan als dictionary is handig maar er ontstaan problemen
# wanneer de dicts in een set worden opgeslagen (sequentie van gamestates)
# waarschijnlijk moeten we een andere manier vinden om het op te slaan
# zodat de gamestates in een set kunnen worden opgeslagen...
#########
class Board(object):
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

	def get_up(self, pos):
		posx = pos[0]
		posy = pos[1]
		if posy > 0:
			return (posx,posy-1)
	def get_down(self, pos):
		posx = pos[0]
		posy = pos[1]
		if posy < self.dimensions -1:
			return (posx,posy+1)
	def get_left(self, pos):
		posx = pos[0]
		posy = pos[1]
		if posx > 0:
			return (posx-1,posy)
	def get_right(self, pos):
		posx = pos[0]
		posy = pos[1]
		if posx < self.dimensions -1:
			return (posx+1,posy)

	def check_moveability(self, auto):
	  # returns an empty list when the car is immovable
	  # otherwise returns all top-left positions 
	  # the car could take (first position)
	  # in a list
		new_top_pos_list = []
		front = self.gamestate[auto][0]
		end = self.gamestate[auto][-1]
		if auto.get_direction() == "v":
			up = self.get_up(front)
			down = self.get_down(end)
			if up != None:
				if self.is_empty(up):
					new_top_pos_list.append(up)
			if down != None:
			    if self.is_empty(down):
					new_top_pos_list.append(self.get_down(front))
		else:
			left = self.get_left(front)
			right = self.get_right(end)
			if left != None:
				if self.is_empty(left):
					new_top_pos_list.append(left)
			if right != None:
			    if self.is_empty(right):
					new_top_pos_list.append(self.get_right(front))
		print "--in check: ", new_top_pos_list
		return new_top_pos_list
	
	def get_new_positions(self, auto, new_top_pos):
		# retuns a list of position which are taken by the car
		# starting from the top left position the car stands on
		pos_list = [new_top_pos]
		if auto.get_direction() == "h":
			for i in range(auto.length-1):
				p = pos_list[i]
				pos_list.append((p[0]+1,p[1]))
		else:
			for i in range(auto.length-1):
				p = pos_list[i]
				pos_list.append((p[0],p[1]+1))

		return tuple(pos_list)

	def move_auto(self, auto, new_top_pos):
		# Changes position of car in gamestate dictionary to the pos_list given
		# and the difference will be used to update all empty fields?
		# top_pos : new top-left position for the car
		gamestate = self.gamestate.copy()
		old_pos = gamestate[auto]
		new_pos = self.get_new_positions(auto,new_top_pos)
		
		new_empty = list(self.empty)
		# self.gamestate[auto] = new_pos
		for i in old_pos:
			if not (i in new_pos):
				new_empty.append(i)
				break
		for i in new_pos:
			if not (i in old_pos):
				new_empty.remove(i)
				break
		gamestate[auto] = new_pos
		return Board(self.dimensions, gamestate, new_empty, self.exit)

	def get_gamestate_tuple(self):
		return tuple(self.gamestate.values())
	def is_empty(self, pos):
		# Returns True if a position is empty, False if it is taken.
		return pos in self.empty
	def __eq__(self,other):
		return self.gamestate == other.gamestate
	def __hash__(self):
	 	return self.get_gamestate_tuple().__hash__()


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
			pos_list.append((p[0]+1,p[1])) ###
	else:
		for i in range(auto.length-1):
			p = pos_list[i]
			pos_list.append((p[0],p[1]+1)) ####

	return tuple(pos_list)

def generate_all_positions(dimensions):
	all_pos = []
	for i in range(dimensions):
		for j in range(dimensions):
			all_pos.append((i,j))
	return all_pos


def load_game(gamefilename):
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
	        top_pos = (x,y)
	        if line_elements[-1] == 'red':
				color = 'red'
				if board_dimensions%2 == 0:
					exit = board_dimensions/2
				else:
					exit = board_dimensions/2 +1
				exit_pos = (x,exit)
	        else:
	        	color = None
	        car_id += 1
	        car = Auto(direction,length,color,car_id)
	        taken_positions = assign_positions(car,top_pos)
	        
	        gamestate[car] = taken_positions
	        for i in taken_positions:
	        	empty_pos.remove(i)
	return board_dimensions, gamestate, empty_pos, exit_pos


def visualize(BB):
    cars_pos = load_game(game)
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

    ###############
    # lijkt allemaal goed te werken nu:
    ###############    
	game = "game_new.txt"
	dim, gs, em, ex = load_game(game)

	BB = Board(dim, gs, em, ex)
    # visualize(BB)
	# for i in gs:
	# 	print i, " : ", gs[i]
	# 	print gs[i][-1] in ep
	gs1 = set()
	gs2 = set()
	gs3 = set()

	# print BB.gamestate
	# print BB.get_gamestate_tuple()
	# for i in BB.gamestate:
	# 	print i
	# 	car = i
	# 	print BB.check_moveability(car)
	B1 = BB
	B2 = BB
	B3 = BB
	for i in BB.gamestate:
		car = i
		moves = BB.check_moveability(car)
		print "moves: ",moves
		if len(moves)>0:
			B1 = B1.move_auto(car,moves[0])
			B2 = B2.move_auto(car,moves[0])
			if len(moves)>1:
				print "jaaaaaa"
				B3 = B3.move_auto(car,moves[1])
			else:
				B3 = B3.move_auto(car,moves[0])
			print "a state:"
			print B1.get_gamestate_tuple()
			print B2.get_gamestate_tuple()
			print B3.get_gamestate_tuple()
			print "b1 ==b2", B1 == B2
			print "b1 == b3", B1 == B3
			gs1.add(B1)
			gs2.add(B2)
			gs3.add(B3)

	print "g1 = g2? y: ", gs1 == gs2
	print "g1 = g3? n: ", gs1 == gs3
	print "all in gs3:"
	for i in gs3:
		print i.get_gamestate_tuple()


	for i in gs1:
		print "i.gs: ", i.get_gamestate_tuple()
		print "1:", i in gs1
		print "2:" ,i in gs2
		print "3:" ,i in gs3

	print "lengths of gs:"
	print len(gs1)
	print len(gs2)
	print len(gs3)





