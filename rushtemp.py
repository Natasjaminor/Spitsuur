import time
# import rushvisua

# Gamestate will be pos_dict pos as key
# value is 0 if no car is in it
# else: car or int refering to auto-id
class Board(object):
    """
	Represents a board with moveable car objects (auto) and an exit.
	"""

    def __init__(self, dimensions, gamestate, empty_pos, car_list, exit_pos):
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
        self.cars = car_list
        self.directions_list = [self.check_left, self.check_right, self.check_up, self.check_down]
        self.directions_strings = ["left", "right", "up", "down"]

    def check_up(self, car):
        if car.direction != "v":
            return False, None
        if car.y[0] - 1 < 0:
            return False, None
        pos = (car.x, car.y[0] - 1)
        if self.gamestate[pos] == 0:
            return True, None
        return False, self.gamestate[pos]  # Car is blocked by a car

    def check_down(self, car):
        if car.direction != "v":
            return False, None
        if car.y[-1] + 1 > self.dimensions:
            return False, None
        pos = (car.x, car.y[-1] + 1)
        if self.gamestate[pos] == 0:
            return True, None
        return False, self.gamestate[pos]  # Car is blocked by a car

    def check_left(self, car):
        if car.direction != "h":
            return False, None
        if car.x[0] - 1 < 0:
            return False, None
        pos = (car.x[0] - 1, car.y)
        if self.gamestate[pos] == 0:
            return True, None
        return False, self.gamestate[pos]  # Car is blocked by a car

    def check_right(self, car):
        if car.direction != "h":
            return False, None
        if car.x[-1] + 1 > self.dimensions:
            return False, None
        pos = (car.x[-1] + 1, car.y)
        if self.gamestate[pos] == 0:
            return True, None
        return False, self.gamestate[pos]  # Car is blocked by a car

    def check_moveability(self, car):
        moves = []
        blocking = []

        for i in self.directions_list:
            result, blocked_by = i(car)
            if result:
                moves.append(self.directions_strings[self.directions_list.index(i)])
            if blocked_by != None:
                blocking.append(blocked_by)

        return moves, blocking

    def get_new_positions(self, auto, new_top_pos):
        # retuns a list of position which are taken by the car
        # starting from the top left position the car stands on
        pos_list = [new_top_pos]
        if auto.get_direction() == "h":
            for i in range(auto.length - 1):
                p = pos_list[i]
                pos_list.append((p[0] + 1, p[1]))
        else:
            for i in range(auto.length - 1):
                p = pos_list[i]
                pos_list.append((p[0], p[1] + 1))

        return tuple(pos_list)

    def move_auto(self, auto, new_top_pos):
        # Changes position of car in gamestate dictionary to the pos_list given
        # and the difference will be used to update all empty fields?
        # top_pos : new top-left position for the car
        gamestate = self.gamestate.copy()
        old_pos = gamestate[auto]
        new_pos = self.get_new_positions(auto, new_top_pos)

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

    def get_cars(self):
        return self.cars

    def get_gamestate_tuple(self):
        return tuple(self.gamestate.values())

    def is_empty(self, pos):
        # Returns True if a position is empty, False if it is taken.
        return pos in self.empty

    def __repr__(self):
        return str(self.gamestate) + "\n"

    def __eq__(self, other):
        return self.gamestate == other.gamestate

    def __hash__(self):
        return self.get_gamestate_tuple().__hash__()


class Auto:
    def __init__(self, direction, length, color=None, ID=None):
        self.length = length
        self.direction = direction
        self.color = color
        self.ID = ID
        self.x = None
        self.y = None

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

    car_id = 0

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
            print "car:", car_id
            for i in taken_positions:
                empty_pos.remove(i)

    if board_dimensions % 2 == 0:
        exit = board_dimensions / 2
    else:
        exit = board_dimensions / 2 + 1
    exit_pos = (board_dimensions - 1, exit - 1)
    print "ex:",exit_pos
    print ("LOADING FILE in %.3f seconds") % (time.clock() - t1)
    return board_dimensions, pos_dict, empty_pos, exit_pos, car_list


if __name__ == "__main__":
    game = "game_new.txt"
    dim, gs, em, ex,car_list = load_game(game)
    print car_list

    BB = Board(dim, gs, em, car_list, ex)
    c = car_list[2]
    print c.direction, c.x, c.y
    m, b = BB.check_moveability(c)
    print m
    print b

