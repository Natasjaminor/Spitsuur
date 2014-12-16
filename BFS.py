import time
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

    statespace = 0
    while not queue.empty():
        game = queue.get(0)
        last_board = game[-1]
        if not last_board in visited:
            visited.add(last_board)
            for car in last_board.gamestate:
                moves = last_board.check_moveability(car)
                for pos in moves:
                    statespace +=1
                    new_board = last_board.move_auto(car, pos)
                    new_game = list(game)
                    new_game.append(new_board)
                    queue.put(new_game)
                    if car.color == 'red':
                        if new_board.gamestate[car][-1] == last_board.exit:
                            solutions.extend(new_game)
    return statespace


if __name__ == "__main__":
    start_time = time.clock()

    game = "game2.txt"
    # game = ".txt"
    dim, gs, em, ex = load_game(game)

    BB = Board(dim, gs, em, ex)

    a = BFS(BB)
    # visualize(BB, a)

    # print a
    # print type(a[1]), "a"
    # print len(a), '<<<<<<< lengte a'
    # print a

    # visualize(BB, [BB])
    # print ("Puzzle was solved in %d states.") % (len(a) - 1)
    print "sp: ", a
    total_time = time.clock() - start_time
    print ("[-----Finished in %.3f seconds]") % total_time

