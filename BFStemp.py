import time
from rushnew import *
import copy
import Queue


def BFS(startboard):
    # Check all possible moves
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
            for car in last_board.auto_dict:
                moves, blocked = last_board.check_moveability(car)
                for move in moves:
                    new_board = last_board.move(car, move)
                    new_game = list(game)
                    new_game.append(new_board)
                    queue.put(new_game)
                    if car.color == 'red':
                        print "RED CAR IS ON: ", (new_board.auto_dict[car][-1])
                        if (new_board.auto_dict[car][-1]) == last_board.exit:
                            print "found"
                            solutions.extend(new_game)
                            return solutions


def BFS2(startboard):
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
            for car in last_board.auto_dict:
                moves, blocked = last_board.check_moveability(car)
                for pos in moves:
                    new_board = last_board.move(car, pos)
                    new_game = list(game)
                    new_game.append(new_board)
                    queue.put(new_game)
                    if car.color == 'red':
                        if new_board.auto_dict[car][-1] == last_board.exit:
                            print "FOUND"
                            solutions.extend(new_game)
                            return solutions

if __name__ == "__main__":
    start_time = time.clock()

    game = "game1.txt"
    # game = ".txt"
    dim, pd, ex, ad = load_game(game)

    BB = Board(dim,pd,ex,ad)

    a = BFS2(BB)
    # visualize(BB, a)

    # print a
    # print type(a[1]), "a"
    # print len(a), '<<<<<<< lengte a'
    # print a

    # visualize(BB, [BB])

    print ("Puzzle was solved in %d states.") % (len(a) - 1)

    # for i in a:
    #     for c in i.cars:
    #         c.print_position()
    #     print "\n"
    total_time = time.clock() - start_time
    print ("[-----Finished in %.3f seconds]") % total_time

