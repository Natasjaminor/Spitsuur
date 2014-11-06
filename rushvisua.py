from Tkinter import *
import math
import time

class BoardVisualization:
    def __init__(self, width, height, delay = 0.2):
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
       
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        print x1, y1, x2, y2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")

        self.tiles = {}
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i,j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.tiles[(i,j)] = self.canvas.create_rectangle(x1, y1, x2, y2)

        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.canvas.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.canvas.create_line(x1, y1, x2, y2)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_cars(self, x,y,width,height):
        x1,y1 = self._map_coords(x-width,y-height)
        x2,y2 = self._map_coords(x,y)
        print x1, y1, x2, y2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "blue")

    def done(self):
        mainloop()

