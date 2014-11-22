from rush import *
import copy

global count 
count = 0

def runBruteDfs(startboard):
	solutions = []
	gameset = {startboard}
	gamelist = [startboard]

	bruteDFS(startboard,gameset,gamelist,solutions)
	print "in run:number of solutions ", len(solutions)
	return solutions


def bruteDFS(startboard, gameset, gamelist, solutions):
	# for all cars check movability
	# for every car try to move
	# remember the gamestate in the set of gamestates
	# check if the red car is on exit
	# if not go check next car.

	# global count
	# if count >= maxdep:
	# 	return
	
	# count += 1
	if gameset == None:
		gameset = {startboard}

	if solutions == None:
		solutions = []
	
	if len(solutions) > 0:
			if len(solutions[0]) < len(gameset):
				print "skip entirely"
				return

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
				continue # do another move
			new_set = gameset.copy()
			new_list = list(gamelist)
			new_set.add(new_board)
			new_list.append(new_board)
			if len(solutions)>0:
				if len(solutions[0]) < len(new_set):
					# print "            SKIP:", len(new_set),"\n"
					break # stop looking further here, this is not optimal.

			if car.color == 'red': # red_car will be made when game is loaded.
				# print "red:", new_board.gamestate[car][-1]
				if new_board.gamestate[car][-1] == startboard.exit:
					#print "       Found a solution:\n ", len(new_set),"\n"
					if len(solutions) == 0:
						#print "\n first solution\n"
						solutions.append(new_set)
						solutions.append(new_list)
						break
					elif len(solutions[0])== len(new_set):
						#print "\n add!\n"
						break # stop looking further in this branch
					elif len(solutions[0])> len(new_set):
						#print "\n replace\n"
						solutions[0] = new_set
						solutions[1] = new_list
						break # stop looking further in this branch
			bruteDFS(new_board, new_set, new_list,solutions)
			#print solutions	
			#return solutions

if __name__ == '__main__':
	game = "game_new.txt"
	dim, gs, em, ex = load_game(game)

	BB = Board(dim, gs, em, ex)
	sol = runBruteDfs(BB)

	print "Solution: \n",sol
	
	# print "Solution: \n",sol
	# for j in sol[0]:
	# 	print j.gamestate, "\n"

	visualize(BB, sol[1])
