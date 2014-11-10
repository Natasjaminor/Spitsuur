from Tkinter import *
import math
import time
import random

class BoardVisualization:
    def __init__(self, width, height, delay = 1.0):
        #self.num_autos = num_autos
        self.delay = delay
        self.max_dim = max(width, height)
        self.width = width
        self.height = height


        #draw canvas
        self.master = Tk()
        self.canvas = Canvas(self.master, width = 500, height = 500)
        self.canvas.pack()
        self.master.update()

        
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                if i == width - 1 and j == (height/2):
                    x2,y2 = self._map_coords(i,j)
                else:
                    x1, y1 = self._map_coords(i,j)
                    x2, y2 = self._map_coords(i + 1, j + 1)
                    self.tiles[(i,j)] = self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")

        for i in range(width):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.canvas.create_line(x1, y1, x2, y2)
        for i in range(height+1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.canvas.create_line(x1, y1, x2, y2)

        self.cars = None
        self.master.update()


    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x-self.width / 2.0) / self.max_dim),
                250 + 450 * ((y-self.height / 2.0) / self.max_dim))

    def _draw_cars(self, begin_x,begin_y,end_x,end_y, length, direction, color):
        colors = ["blue", "yellow", "green", "purple"]
        x1,y1 = self._map_coords(begin_x,begin_y)
        
        if direction == 'h':
            x2,y2 = self._map_coords(begin_x + length, begin_y + 1)
        else:
            x2,y2 = self._map_coords(begin_x +1, begin_y + length)
        print x1, y1, x2, y2
        if color == "red":
            return self.canvas.create_rectangle(x1, y1, x2, y2, fill = "red", outline ="black")
        else:
            random_color = random.randrange(0,3) 
            return self.canvas.create_rectangle(x1, y1, x2, y2, fill = colors[random_color], outline ="black")


    def update(self, gamestate):
        for state in gamestate:
            game = state.gamestate
            print game, "from Rushvisua gamestate"
    
            #delete existing cars
            if self.cars != None:
                for car in self.cars:
                    self.canvas.delete(car)
                    #self.master.update_idletasks()

            #draw new cars
            self.cars = []
            for coords in game.items():
                car_id = coords[0]
                direction = car_id.direction
                color = car_id.color
                length = car_id.length
                begin_x = coords[1][0][0]
                begin_y = coords[1][0][1]
                end_x =  coords[1][-1][0]
                end_y =  coords[1][-1][1]
                self.cars.append(self._draw_cars(begin_x, begin_y, end_x, end_y, length, direction, color))

        print self.cars, "lijst met autos uit rushvisua"
        self.master.update()
        time.sleep(self.delay)
        
        

    def done(self):
        mainloop()

