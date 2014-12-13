from rush import *
import copy
from Queue import PriorityQueue

# ontvang startboard
# bereken afstand tot exit rode autootje
# bereken distance
# sommeer afstand + distance 
# voeg startboard toe aan priortity queue
# haal startboard uit de queue
# voeg startboard toe aan visited
# distance + 1
# maak kinderen daarvan
# bereken van elk kind afstand tot exit rode autootje + distance
# stop ze in priority queue
# haal weer kind eruit etc.

def solveAStar(startboard, goal):
	parent = startboard
	visited = set()
	solutions = []
	distance = 0

	pq = PriorityQueue()
	totalcost = calctotalcost(parent,goal,distance)
	pq.put((totalcost, [[parent], [distance]])) #totalcost is heuristiek, boardobject met bijbehorende distance in boom
	

	while not pq.empty():
		board = pq.get(0)
		last_board = board[1][0][-1]
		if not last_board in visited:
			visited.add(last_board)
			# kijkt naar zijn plek in de boom qua distance van de parent, 
			# telt er 1 bij op voor de volgende kinderen wordt next_distance
			next_distance = board[1][1][0] + 1  
			for car in last_board.gamestate:
				moves = last_board.check_moveability(car)
				for pos in moves:
					new_board = last_board.move_auto(car, pos)
					new_totalcost = calctotalcost(new_board,goal,next_distance)
					new_game = list(board[1][0])
					new_game.append(new_board)
					pq.put((new_totalcost, [new_game, [next_distance]]))
					if car.color == 'red':
						if new_board.gamestate[car][-1] == last_board.exit:
							solutions.extend(new_game)
							return solutions
			
		
def calctotalcost(node, goal, distance):
	game = node.gamestate
	redcarexit = game.values()[0][1][0]
	manhattendistance = goal[0] - redcarexit
	totalcost = manhattendistance + distance
	return totalcost

		

game = "game2.txt"
dim, gs, em, ex = load_game(game)
BB = Board(dim, gs, em, ex)
a = solveAStar(BB, ex)
print len(a)