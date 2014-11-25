from rush import *
import copy
import Queue

def BFS(startboard):
	#Check all possible moves
	#append these moves to set
	#append these moves to queue, queue.extend()
	#check children of parent (queue.pop(0))
	visited = set()
	queue = Queue.Queue()
	queue.put([startboard])
	solutions = []
	gamelist = []

	
	while not queue.empty():
		game = queue.get(0)
		last_board = game[-1]
		if not last_board in visited:
			visited.add(last_board)
			for car in last_board.gamestate:
				moves = last_board.check_moveability(car)
				for pos in moves:
					new_board = last_board.move_auto(car, pos)
					new_game = list(game)
					new_game.append(new_board)
					queue.put(new_game)
					if car.color == 'red':
						if new_board.gamestate[car][-1] == last_board.exit:
							solutions.extend(new_game)
							return solutions
	

game = "GAME1.txt"
dim, gs, em, ex = load_game(game)

BB = Board(dim, gs, em, ex)

a = BFS(BB)
# print a
# print type(a[1]), "a"
print len(a), '<<<<<<< lengte a'
# print a
visualize(BB, a)

