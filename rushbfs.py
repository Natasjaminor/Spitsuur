from rush import *
import copy
import Queue


def bruteBFS(startboard, start):
	#Check all possible moves
	#append these moves to set
	#append these moves to queue, queue.extend()
	#check children of parent (queue.pop(0))

	# print startboard, "startboard"
	visited = set()
	queue = Queue.Queue()
	queue.put(startboard)
	solutions = []
	gamelist = [startboard]
	# for elem in list(queue.queue):
		# print elem, "firstqueue"

	while not queue.empty():
		game = queue.get(0)
		#print game, "game"
		if not game in visited:
			visited.add(game)
			new_list = list(gamelist)
			#print new_list, "the new_list"
			for car in game.gamestate:
				moves = game.check_moveability(car)
				for pos in moves:
					new_board = game.move_auto(car, pos)
					new_list.append(new_board)
					#print new_list, "new_list"
					#print new_board, "new_board"
					queue.put(new_board)
					if car.color == 'red':
						if new_board.gamestate[car][-1] == game.exit:
							solutions.append(visited)
							solutions.append(new_list)
			#print solutions, "solutions"
	# print list(queue.queue),"queue"

	return solutions	
	#print visited, "visited"





game = "GAME1.txt"
dim, gs, em, ex = load_game(game)

BB = Board(dim, gs, em, ex)
start = BB

a = bruteBFS(BB, start)
# print a
# print type(a[1]), "a"
visualize(BB, a[1])

