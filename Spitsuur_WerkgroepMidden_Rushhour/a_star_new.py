
from rushnew import *
import rushvisuatemp
import copy
from Queue import PriorityQueue
import time

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



def solveAStar(startboard, goal, cars):
    parent = startboard
    visited = set()
    solutions = []
    distance = 0

    pq = PriorityQueue()
    totalcost = calctotalcost(parent, goal, distance,cars)
    pq.put(
        (totalcost, [[parent], [distance]]))  # totalcost is heuristiek, boardobject met bijbehorende distance in boom

    while not pq.empty():
        board = pq.get(0)
        last_board = board[1][0][-1]
        if not last_board in visited:
            visited.add(last_board)
            # kijkt naar zijn plek in de boom qua distance van de parent,
            # telt er 1 bij op voor de volgende kinderen wordt next_distance
            next_distance = board[1][1][0] + 1
            for car in last_board.auto_dict:
                moves,blocked = last_board.check_moveability(car)
                for pos in moves:
                    new_board = last_board.move(car, pos)
                    new_totalcost = calctotalcost(new_board, goal, next_distance,cars)
                    new_game = list(board[1][0])
                    new_game.append(new_board)
                    pq.put((new_totalcost, [new_game, [next_distance]]))
                    if car.color == 'red':
                        if new_board.auto_dict[car][-1] == last_board.exit:
                            solutions.extend(new_game)
                            return solutions


def calctotalcost(board, goal, distance, car_list):
    cars_cost = 0
    conflict_cost = 0

    game = board.auto_dict
    dim = board.dimensions
    pd = board.pos_dict
    rx,ry = game.values()[0][1]  # get tail position car
    manhattendistance = goal[0] - rx

    for i in range(1,dim-rx-1):
        value = pd[(rx+i,ry)]
        if value != 0:
            cars_cost += 1
            # car = car_list[value-1]
            # m,b = board.check_moveability(car)
            # conflict_cost += len(b)
    totalcost = manhattendistance + cars_cost+ distance
    return totalcost


def calculate_blocks(board,car,prev_id_list):
    conflicts = 0
    m,b = board.check_moveability(car)
    if len(b)-1>0:
        conflicts +=1
        for i in b:
            if not (i in prev_id_list):
                prev_id_list.append(i)
                conflicts += calculate_blocks(board,car,prev_id_list)
            else:
                conflicts +=1
        return conflicts
    return 0


def visualize(solutions):
    first_board = solutions[0]
    gamestate = []
    width = int(first_board.dimensions)
    height = int(first_board.dimensions)
    board = rushvisuatemp.BoardVisualization(width, height)

    for i in solutions:
        gamestate.append(i)
        board.update([i])
        board.update(solutions)
    board.done()

if __name__ == "__main__":
    start_time = time.clock()
    game = "game3.txt"
    dim, pd, ex, ad, cars = load_game(game)
    BB = Board(dim,pd,ex,ad)

    calctotalcost(BB,ex,0,cars)
    visualize([BB])
    a = solveAStar(BB, ex,cars)

    print ("Puzzle was solved in %d states.") % (len(a) - 1)
    total_time = time.clock() - start_time
    print ("[-----Finished in %.3f seconds]") % total_time
