import time
import rushvisuatemp

# Gamestate will be pos_dict pos as key
# value is 0 if no car is in it
# else: car or int refering to auto-id
class Board(object):
    """
	Represents a board with moveable car objects (auto) and an exit.
	"""

    def __init__(self, dimensions, pos_dict, exit_pos, auto_dict):
        """
	  Initializes the board with its dimensions. The initial
	  gamestate,exit and emptyfields are stored.
	  dimensions: integer
	  gamestate: dictionary -> key; auto ,
		   value; list of occupied positions as Position.
	  empty_pos: set of Position objects on the board that are empty.

	  """
        self.dimensions = dimensions
        self.pos_dict = pos_dict
        self.auto_dict = auto_dict
        self.exit = exit_pos

        self.checks_dict = {"left":self.check_left,"right": self.check_right,
                       "up": self.check_up, "down": self.check_down}

    def check_up(self, car):
        pos = self.auto_dict[car][0] #head
        pos = self.get_up(pos)
        if car.direction != "v":
            return False, None
        if pos == None:
            return False, None
        if self.pos_dict[pos] == 0:
            return True, None
        return False, self.pos_dict[pos]  # Car is blocked by a car

    def check_down(self, car):
        pos = self.auto_dict[car][-1] #tail
        pos = self.get_down(pos)
        if car.direction != "v":
            return False, None
        if pos == None:
            return False, None
        if self.pos_dict[pos] == 0:
            return True, None
        return False, self.pos_dict[pos]  # Car is blocked by a car

    def check_left(self, car):
        pos = self.auto_dict[car][0] #head
        pos = self.get_left(pos)
        if car.direction != "h":
            return False, None
        if pos == None:
            return False, None
        if self.pos_dict[pos] == 0:
            return True, None
        return False, self.pos_dict[pos]  # Car is blocked by a car

    def check_right(self, car):
        pos = self.auto_dict[car][-1] #tail
        pos = self.get_right(pos)
        if car.direction != "h":
            return False, None
        if pos == None:
            return False, None
        if self.pos_dict[pos] == 0:
            return True, None
        return False, self.pos_dict[pos]  # Car is blocked by a car

    def check_moveability(self, car):
        moves = []
        blocking = []

        # Check if a car can move left,right,up,down:
        for i in self.checks_dict:
            f = self.checks_dict[i]
            result, blocked_by = f(car)
            if result:
                moves.append(i)
            if blocked_by != None:
                blocking.append(blocked_by)

        return moves, blocking

    def get_up(self, pos):
        posx = pos[0]
        posy = pos[1]
        if posy > 0:
            return (posx, posy - 1)

    def get_down(self, pos):
        posx = pos[0]
        posy = pos[1]
        if posy < self.dimensions - 1:
            return (posx, posy + 1)

    def get_left(self, pos):
        posx = pos[0]
        posy = pos[1]
        if posx > 0:
            return posx - 1, posy

    def get_right(self, pos):
        posx = pos[0]
        posy = pos[1]
        if posx < self.dimensions - 1:
            return (posx + 1, posy)

    def move(self,auto,movestring):
        do_dict= {"left":self.get_left, "right":self.get_right,
                  "up": self.get_up, "down":self.get_down}
        pd = self.pos_dict.copy()
        ad = self.auto_dict.copy()
        positions = ad[auto]
        new_positions =[]
        for p in positions:
            v = do_dict[movestring]
            v = v(p)
            new_positions.append(v)
            pd[p] = 0
        for p in new_positions:
            pd[p] = auto.ID

        ad[auto] = tuple(new_positions)
        return Board(self.dimensions,pd,self.exit,ad)

    def get_pos_tuple(self):
        return tuple(self.pos_dict.items())

    def get_auto_tuple(self):
        return tuple(self.auto_dict.values())

    def is_empty(self, pos):
        # Returns True if a position is empty, False if it is taken.
        return self.pos_dict[pos] == 0

    def __repr__(self):
        return str(self.pos_dict) + "\n"

    def __eq__(self, other):
        return self.pos_dict == other.pos_dict

    def __hash__(self):
        return self.get_pos_tuple().__hash__()


class Auto:
    def __init__(self, direction, length, color=None, ID=None):
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

    def __ne__(self, other):
        return self.ID != other.ID

    def __hash__(self):
        return hash(self.ID)

    def __repr__(self):
        if self.color != None:
            return "AUTO-ID(" + str(self.ID) + ")" + "(-RED-)"
        return "AUTO-ID(" + str(self.ID) + ")"


def set_auto_pos(positions, auto):
    direction = auto.get_direction()
    x = []
    y = []

    if direction == "v":
        for i in positions:
            x = i[0]
            y.append(i[1])
    else:
        for i in positions:
            x.append(i[0])
            y = i[1]

    auto.x, auto.y = x, y


def generate_all_positions(dimensions):
    all_pos = []
    pos_dict = {}
    for i in range(dimensions):
        for j in range(dimensions):
            all_pos.append((i, j))
            pos_dict[(i, j)] = 0
    return all_pos, pos_dict


def assign_positions(auto, top_pos):
    # retuns a list of position which are taken by the car
    # starting from the top left position the car stands on
    pos_list = [top_pos]
    if auto.get_direction() == "h":
        for i in range(auto.length - 1):
            p = pos_list[i]
            pos_list.append((p[0] + 1, p[1]))  # ##
    else:
        for i in range(auto.length - 1):
            p = pos_list[i]
            pos_list.append((p[0], p[1] + 1))  # ###

    return tuple(pos_list)


def load_game(gamefilename):
    t1 = time.clock()
    inputFile = open(gamefilename)
    gamestate = {}
    car_list = []
    pos_dict = {}

    car_id = 1

    for line in inputFile:
        line_elements = line.strip()
        line_elements = line_elements.split(" ")
        if line_elements[0] == '*' or line_elements[0] == '':
            continue

        elif line_elements[0] == '#':
            board_dimensions = int(line_elements[1])
            empty_pos, pos_dict = generate_all_positions(board_dimensions)

        else:
            direction = line_elements[0]
            length = int(line_elements[1])
            x = int(line_elements[2])
            y = int(line_elements[3])
            top_pos = (x, y)

            if line_elements[-1] == 'red':
                color = 'red'
            else:
                color = None

            car = Auto(direction, length, color, car_id)
            car_list.append(car)

            car_id += 1
            taken_positions = assign_positions(car, top_pos)
            gamestate[car] = taken_positions

            for i in taken_positions:
                pos_dict[i] = car.ID
            set_auto_pos(taken_positions, car)
            for i in taken_positions:
                empty_pos.remove(i)

    if board_dimensions % 2 == 0:
        exit = board_dimensions / 2
    else:
        exit = board_dimensions / 2 + 1
    exit_pos = (board_dimensions - 1, exit - 1)
    print ("LOADING FILE in %.3f seconds") % (time.clock() - t1)
    return board_dimensions, pos_dict,exit_pos, gamestate,car_list


if __name__ == "__main__":

    game = "game_small.txt"
    dim, pd, ex,ad, cars = load_game(game)
    print car_list

    BB = Board(dim,pd,ex,ad)
    visualize
