from rush import *

global count 
count = 0

def runBruteDfs(startboard):
	solutions = []
	gameset = {startboard}

	bruteDFS(startboard,gameset,solutions)
	return solutions

# TO DO:
# implement length check.
def bruteDFS(startboard, gameset, solutions, maxdep = 50):
	# for all cars check movability
	# for every car try to move
	# remember the gamestate in the set of gamestates
	# check if the red car is on exit
	# if not go check next car.
	global count
	if count >= maxdep:
		return
	
	count += 1
	if gameset == None:
		gameset = {startboard}

	if solutions == None:
		solutions = []
	
	for car in startboard.gamestate:
		moves = startboard.check_moveability(car)
		for pos in moves:
			# do the move and make a new board
			# is it in set? --> end
			# is the red car on the exit?
			# add it to the solutions.
			# go on recursively
			new_board = startboard.move_auto(car, pos)

			if new_board in gameset:
				continue
			
			gameset.add(new_board)
			if car.color == 'red': # red_car will be made when game is loaded.
				if startboard.gamestate[car][-1] == startboard.exit:
					# print "found a solution: ", gameset
					solutions.append(gameset)
			new_set = gameset.copy()
			bruteDFS(new_board, new_set, solutions)
			print solutions		
			return solutions

if __name__ == '__main__':
	game = "game_new.txt"
	dim, gs, em, ex = load_game(game)

	BB = Board(dim, gs, em, ex)
	runBruteDfs(BB)
	sol = runBruteDfs(BB)
	for i in sol:
		if len(i) < 50:
			print i
	# print "done"








