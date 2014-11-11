
# Tkinter zit standaard in python xy
import Tkinter

class Visualization:
    def __init__(self, num_autos, width, height):
        self.num_autos = num_autos
        self.width = width
        self.height = height

    self.root = Tkinter.Tk()
    self.canvas = Tkinter.Canvas(self.root, width = 500, height = 500)
    self.canvas.pack()
    self.root.update()


for row in range(6): # maakt rijen en kolommen
    for column in range(6):
        canvas.create_line(50 *column, 0, 50 * column, 400)
    for row in range(6):
        canvas.create_line(0, 50 * row, 400, 50 * row)

canvas.create_rectangle(150, 0, 100, 150, fill="purple") # Een auto

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))



root.mainloop()
